import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

# 定义输入和输出文件夹
input_folder = r'E:\0_Immortal\IMMO-04 Pics\三次元 Model'
output_folder = r'D:\Work\convert\cache\三次元 Model'
error_log_file = r'D:\Work\convert\error_log.txt'


# 定义处理单个文件的函数
def process_file(input_file, output_file, extension):
    temp_output_file = output_file + '.tmp'

    # 删除可能存在的临时文件
    if os.path.exists(temp_output_file):
        os.remove(temp_output_file)

    try:
        if extension in ('.jpg', '.jpeg'):
            # 构建 cjpeg 命令
            cjpeg_command = ['cjpegli', input_file, temp_output_file, '-q', '90', '--chroma_subsampling=444']
            # 调用 cjpeg 命令
            subprocess.run(cjpeg_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # 使用 exiftool 添加 XMP 元数据
            add_xmp_command = ['exiftool', '-overwrite_original', '-xmp:description=compressed', temp_output_file]
            subprocess.run(add_xmp_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif extension in ('.png', '.bmp'):
            # 构建 cwebp 命令
            cwebp_command = ['cwebp', '-q', '50', '-lossless', '-sharp_yuv', input_file, '-o', temp_output_file]
            # 调用 cwebp 命令
            subprocess.run(cwebp_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # 使用 exiftool 添加 XMP 元数据
            add_xmp_command = ['exiftool', '-overwrite_original', '-xmp:description=compressed', temp_output_file]
            subprocess.run(add_xmp_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            # 其他类型文件，直接复制到临时文件
            shutil.copy2(input_file, temp_output_file)

        # 将临时文件重命名为最终文件
        os.rename(temp_output_file, output_file)

    except (subprocess.CalledProcessError, IOError) as e:
        if os.path.exists(temp_output_file):
            os.remove(temp_output_file)
        with open(error_log_file, 'a', encoding='utf-8') as log:
            log.write(f"Error processing {input_file}: {e}\n")


# 遍历文件夹函数
def convert_images(input_dir, output_dir):
    tasks = []
    processed_count = 0
    total_files = sum(len(files) for _, _, files in os.walk(input_dir))

    with ThreadPoolExecutor(max_workers=5) as executor:
        for root, dirs, files in os.walk(input_dir):
            for filename in files:
                input_file = os.path.join(root, filename)
                _, extension = os.path.splitext(filename)
                extension = extension.lower()

                if extension in ('.jpg', '.jpeg', '.png', '.bmp'):
                    relative_path = os.path.relpath(input_file, input_dir)
                    output_file = os.path.join(output_dir, relative_path)
                    if extension in ('.png', '.bmp'):
                        output_file = os.path.splitext(output_file)[0] + '.webp'
                    else:
                        output_file = output_file[:-len(extension)] + extension

                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    if not os.path.exists(output_file):
                        tasks.append(executor.submit(process_file, input_file, output_file, extension))
                else:
                    relative_path = os.path.relpath(input_file, input_dir)
                    output_file = os.path.join(output_dir, relative_path)
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    if not os.path.exists(output_file):
                        tasks.append(executor.submit(process_file, input_file, output_file, extension))

        for future in as_completed(tasks):
            try:
                future.result()
                processed_count += 1
                if processed_count % 10 == 0:
                    print(f"\rProcessed {processed_count} files out of {total_files} total files", end='', flush=True)
                    sys.stdout.flush()
            except Exception as e:
                continue

    # 最后打印完成信息
    print(f"\rProcessed {processed_count} files out of {total_files} total files")
    sys.stdout.flush()


# 执行转换或复制
convert_images(input_folder, output_folder)