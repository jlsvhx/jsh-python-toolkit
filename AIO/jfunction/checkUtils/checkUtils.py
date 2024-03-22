# https://github.com/ftarlao/check-media-integrity
# ffmpeg-python==0.1.17
# future==0.17.1
# Pillow-SIMD==5.3.0.post0
# PyPDF2==1.26.0
# Wand==0.4.5
# ImageMagick-6.9.13-7-Q16-HDRI-x64-dll.exe
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Queue, Process
from queue import Empty
from subprocess import Popen, PIPE
from tkinter import filedialog

# import cv2  # py-opencv
import sqlite3
import zlib
import ffmpeg
# import imageio
from PIL import Image
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from pillow_heif import register_heif_opener, register_avif_opener  # pip3 install pillow-heif
import threading

register_heif_opener()
register_avif_opener()
Image.MAX_IMAGE_PIXELS = None  # 禁用解压缩炸弹限制

VIDEO_EXTENSIONS = {'avi', 'mp4', 'mov', 'mpeg', 'mpg', 'm2p', 'mkv', '3gp', 'ogg', 'flv', 'f4v', 'f4p', 'f4a', 'f4b'}

IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'heif', 'heic', 'jp2', 'ico', 'svg', 'eps',
                    'psd', 'hdr', 'pict', 'pct'}


# 插入文件名和CRC32值到数据库
def insert_file_crc32(filename, crc32_value):
    # 创建一个SQLite数据库连接
    conn = sqlite3.connect('crc32_database.db')
    cursor = conn.cursor()

    # 创建一个表来存储文件名和对应的CRC32值
    cursor.execute('''CREATE TABLE IF NOT EXISTS imagecrc
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       filename TEXT UNIQUE,
                       crc32 INTEGER)''')

    cursor.execute("INSERT INTO files (filename, crc32) VALUES (?, ?)", (filename, crc32_value))
    conn.commit()

    # 检查图像文件名是否已存在于数据库中
    def is_image_in_database(filename):
        cursor.execute("SELECT COUNT(*) FROM imagecrc WHERE filename=?", (filename,))
        result = cursor.fetchone()
        return result[0] > 0


def get_extension(filename):
    file_lowercase = filename.lower()
    return os.path.splitext(file_lowercase)[1][1:]


# 计算文件的CRC32值
def calculate_crc32(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
            crc32_value = zlib.crc32(data)
            return crc32_value
    except Exception as e:
        print(f"Error calculating CRC32 for {file_path}: {e}")
        return None


def magick_identify_check(filename):
    proc = Popen(['identify', '-regard-warnings', filename], stdout=PIPE,
                 stderr=PIPE)  # '-verbose',
    out, err = proc.communicate()
    exitcode = proc.returncode
    if exitcode != 0:
        raise Exception('Identify error:' + str(err))
    return out


def pil_check(filename):
    img = Image.open(filename)  # open the image file
    img.verify()  # verify that it is a good image, without decoding it.. quite fast
    img.close()


def check_size(filename, zero_exception=True):
    statfile = os.stat(filename)
    filesize = statfile.st_size
    if filesize == 0 and zero_exception:
        raise SyntaxError("Zero size file")
    return filesize


def ffmpeg_check(filename, error_detect='default', threads=0):
    if error_detect == 'default':
        stream = ffmpeg.input(filename)
    else:
        if error_detect == 'strict':
            custom = '+crccheck+bitstream+buffer+explode'
        else:
            custom = error_detect
        stream = ffmpeg.input(filename, **{'err_detect': custom, 'threads': threads})

    stream = stream.output('pipe:', format="null")
    stream.run(capture_stdout=True, capture_stderr=True)


def check_file(filename, strict_level=2):
    try:
        # check_size(filename)
        if strict_level in [0, 1]:
            pil_check(filename)
        if strict_level in [0, 2]:
            magick_identify_check(filename)

        # if get_extension(filename) in VIDEO_EXTENSIONS:
        #     ffmpeg_check(filename)

    except Exception as e:
        return (filename, str(e)), False  # 图片损坏

    return (filename, None), True  # 图片完整


def check_broken_images_in_folder_mu(folder_path):
    strict_level = 2
    """
    检查输入目录下有多少损坏的图像文件，并将信息写入到输入目录下的corrupted_images.txt（多线程）
    :param folder_path:
    :return:
    """

    corrupted_path = os.path.join(folder_path, 'corrupted_images.txt')
    intact_path = os.path.join(folder_path, 'intact_images.txt')
    non_image_path = os.path.join(folder_path, 'non_image_files.txt')

    with open(corrupted_path, 'w', encoding='utf-8') as corrupted_file, \
            open(intact_path, 'w', encoding='utf-8') as intact_file, \
            open(non_image_path, 'w', encoding='utf-8') as non_image_file:

        # 创建线程池
        with ThreadPoolExecutor(5) as executor:
            # 存储所有任务的 Future 对象
            futures = []
            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    image_path = os.path.join(root, filename)
                    file_ext = get_extension(filename)
                    if file_ext in IMAGE_EXTENSIONS:
                        # 提交图像处理任务到线程池，并收集 Future 对象
                        future = executor.submit(check_file, image_path, strict_level)
                        futures.append(future)
                    else:
                        non_image_file.write(f"文件 {image_path} 不是图像文件！\n")

            # 处理所有任务的结果
            for future in as_completed(futures):
                detail, is_success = future.result()
                if is_success:
                    # 如果需要，可以在这里处理完整的图像
                    pass
                else:
                    print(f"图像 {detail[0]} 损坏！{detail[1]}")
                    corrupted_file.write(f"图像 {image_path} 损坏！{detail[1]}\n")

    print("检查损坏图片 完成")


def delete_corrupted_images(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # 使用正则表达式提取图像路径
            match = re.search(r'图像\s(.*?)\s损坏！', line)
            if match:
                image_path = match.group(1)
                # 删除图像文件
                try:
                    # os.remove(image_path)
                    print(f"已删除损坏图像文件：{image_path}")
                except Exception as e:
                    print(f"删除图像文件时出错：{e}")


def delete_and_mark_corrupted_images(file_path):
    text_file = os.path.join(file_path, 'corrupted_images.txt')
    with open(text_file, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        f.seek(0)  # 将文件指针移到文件开头
        for line in lines:
            # 使用正则表达式提取图像路径
            match = re.search(r'(图像\s.*?)\s损坏！', line)
            if match:
                image_path = match.group(1)
                # 删除图像文件并在原文本中追加信息
                try:
                    # os.remove(image_path)
                    f.write(match.group(0) + ' 已删除\n')
                    print(f"已删除损坏图像文件：{image_path}")
                except Exception as e:
                    print(f"删除图像文件时出错：{e}")
            else:
                f.write(line)  # 将未损坏的行写回文件
        f.truncate()  # 截断文件，删除多余内容


def process_image2(image_path):
    try:
        img = Image.open(image_path)
        img.verify()
        img.close()
        return image_path, False  # 图像未损坏
    except Exception as e:
        pass

    # try:
    #     img = cv2.imread(image_path)
    #     if img is None:
    #         pass
    #     else:
    #         return image_path, False  # 图像未损坏
    # except Exception as e:
    #     pass

    # try:
    #     # 尝试读取图像文件
    #     with open(image_path, 'rb') as f:
    #         im = imageio.v3.imread(f)
    #     return image_path, False  # 图像文件正常
    # except Exception as e:
    #     pass

    return image_path, True  # 图像损坏


if __name__ == '__main__':
    calculate_crc32_in_folder_mu('pic')

