import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from subprocess import Popen, PIPE
from tkinter import filedialog

# import cv2  # py-opencv
import sqlite3
import zlib

# import imageio
from PIL import Image
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from pillow_heif import register_heif_opener, register_avif_opener  # pip3 install pillow-heif
import threading

register_heif_opener()
register_avif_opener()
Image.MAX_IMAGE_PIXELS = None  # 禁用解压缩炸弹限制


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

    # # Image manipulation is mandatory to detect few defects
    # img = Image.open(filename)  # open the image file
    # # alternative (removed) version, decode/recode:
    # # f = cStringIO.StringIO()
    # # f = io.BytesIO()
    # # img.save(f, "BMP")
    # # f.close()
    # img.transpose(Image.FLIP_LEFT_RIGHT)
    # img.close()


def check_file(filename, strict_level=2):
    try:
        if strict_level in [0, 1]:
            pil_check(filename)
        if strict_level in [0, 2]:
            magick_identify_check(filename)

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
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp',
                        '.heif', '.heic', '.jp2', '.ico',
                        '.svg', '.eps', '.psd', '.hdr', '.pict', '.pct'}

    corrupted_path = os.path.join(folder_path, 'corrupted_images.txt')
    intact_path = os.path.join(folder_path, 'intact_images.txt')
    non_image_path = os.path.join(folder_path, 'non_image_files.txt')

    with open(corrupted_path, 'w', encoding='utf-8') as corrupted_file, \
            open(intact_path, 'w', encoding='utf-8') as intact_file, \
            open(non_image_path, 'w', encoding='utf-8') as non_image_file:

        # 创建线程池
        with ThreadPoolExecutor() as executor:
            # 存储所有任务的 Future 对象
            futures = []
            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    image_path = os.path.join(root, filename)
                    _, file_ext = os.path.splitext(filename)
                    file_ext = file_ext.lower()
                    if file_ext in image_extensions:
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
                    print(f"图像 {detail[0]} 损坏！{detail[1]}\n")
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


def calculate_crc32_in_folder_mu(main_directory, thread_count=1):
    """
    校检输入目录下的sfv文件中存储的crc32值是否和文件计算出来的一致（多线程）

    如果文件不存在对应crc32，则计算并存入sfv文件中

    如果sfv文件不存在，则创建新sfv文件，并计算文件的crc32存入sfv文件中

    :param main_directory:
    :param thread_count:
    :return:
    """

    def is_exclude_file(name):
        if name.endswith('.sfv'):
            return True
        if name.endswith('.ffs_db'):
            return True
        if 'non_image_files' in name or 'intact_images' in name or 'corrupted_images' in name:
            return True
        return False

    def is_exclude_sfv_line(line):
        if 'Generated by WIN-SFV32' in line or 'Compatible: EF CheckSum Manager' in line:
            return True
        if 'non_image_files' in line or 'intact_images' in line or 'corrupted_images' in line:
            return True
        return False

    def create_sfv(svf_located_folder_apath):
        file_list = os.listdir(svf_located_folder_apath)
        files_only_set = set()
        for f in file_list:
            if os.path.isfile(os.path.join(svf_located_folder_apath, f)):
                files_only_set.add(os.path.join(svf_located_folder_apath, f))

        if len(files_only_set) > 0:
            sfv_file_apath = os.path.join(svf_located_folder_apath, os.path.basename(svf_located_folder_apath) + '.sfv')
            with open(sfv_file_apath, 'w', encoding='utf-8') as svf:
                print(f"{sfv_file_apath} 不存在，创建中")
                for file in files_only_set:
                    file_name = os.path.basename(file)
                    if is_exclude_file(file_name):
                        continue
                    with open(file, 'rb') as f:
                        content = f.read()
                        crc32_calculated = zlib.crc32(content)
                        line = file_name + " " + '{:08x}'.format(crc32_calculated & 0xFFFFFFFF) + "\n"
                        svf.write(line)

    def process_sfv_file(svf_file_apath):
        svf_located_folder_apath = os.path.dirname(svf_file_apath)
        file_list = os.listdir(svf_located_folder_apath)
        files_only_set = set()
        for f in file_list:
            if os.path.isfile(os.path.join(svf_located_folder_apath, f)):
                files_only_set.add(os.path.join(svf_located_folder_apath, f))

        with open(svf_file_apath, 'r', encoding='utf-8') as file:

            for line in file:

                if is_exclude_sfv_line(line):
                    continue

                filename, crc32_value = line.rsplit(' ', 1)

                crc32_value = crc32_value.rstrip('\n')

                filename = os.path.join(os.path.dirname(svf_file_apath), filename)  # 获取文件的绝对路径

                if filename.endswith(".sfv"):
                    continue
                if os.path.exists(filename):
                    files_only_set.remove(filename)
                    with open(filename, 'rb') as f:
                        content = f.read()
                        crc32_calculated = zlib.crc32(content)
                    if '{:08x}'.format(crc32_calculated & 0xFFFFFFFF) == crc32_value.lower():
                        # print(f"文件 '{filename}' 的CRC32值验证通过")
                        pass
                    else:
                        print(f"文件 '{filename}' 的CRC32值验证未通过")
                else:
                    print(f"文件 '{filename}' 不存在")

        if len(files_only_set) > 0:
            with open(svf_file_apath, 'a', encoding='utf-8') as svf:
                for file in files_only_set:
                    file_name = os.path.basename(file)
                    if file_name.endswith(".sfv"):
                        continue
                    with open(file, 'rb') as f:
                        content = f.read()
                        crc32_calculated = zlib.crc32(content)
                        line = file_name + " " + '{:08x}'.format(crc32_calculated & 0xFFFFFFFF) + "\n"
                        svf.write(line)

    def process_sfv_files_in_directory(directory):
        flag = 0
        for item in os.listdir(directory):
            if item.endswith('.sfv'):
                sfv_file_path = os.path.join(directory, item)
                flag = 1
                process_sfv_file(sfv_file_path)
        if flag == 0:
            create_sfv(directory)

    # 获取CPU核心数
    cpu_cores = os.cpu_count()
    thread_count = cpu_cores * 2

    all_dirs = [main_directory]

    # 构建要处理的文件夹列表
    for root, dirs, files in os.walk(main_directory):
        for dir in dirs:
            all_dirs.append(os.path.join(root, dir))

    work_size = len(all_dirs) // thread_count + 1
    # 用于存储要处理的文件夹列表
    folders_to_process = [all_dirs[i:i + work_size] for i in range(0, len(all_dirs), work_size)]

    # 多线程处理
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for folders in folders_to_process:
            executor.map(process_sfv_files_in_directory, folders)

    print("计算CRC32 完成")


def open_current_sfv(dir):
    if os.path.isdir(dir):
        dirname = os.path.basename(dir)
        sfvname = dirname + '.sfv'
        sfvpath = os.path.join(dir, sfvname)
        if os.path.exists(sfvpath):
            QDesktopServices.openUrl(QUrl.fromLocalFile(sfvpath))


def is_svf_exist(dir):
    if os.path.isdir(dir):
        dirname = os.path.basename(dir)
        sfvname = dirname + '.sfv'
        sfvpath = os.path.join(dir, sfvname)
        if os.path.exists(sfvpath):
            return True
    return False


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
    check_broken_images_in_folder_mu('pic')

