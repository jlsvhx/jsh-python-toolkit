import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义输入和输出文件夹
input_folder = r'E:\0_Immortal\IMMO-04 Pics\2次元 角色'
output_folder = r'D:\Work\convert\cache\2次元 角色'
error_log_file = r'D:\Work\convert\2次元error_log.txt'

# 定义处理单个文件的函数
def process_file(input_file, output_file, extension):
    try:
        if extension in ('.jpg', '.jpeg'):
            # 构建 cjpeg 命令
            cjpeg_command = ['cjpegli', input_file, output_file, '-q', '90']
            # 调用 cjpeg 命令
            subprocess.run(cjpeg_command, check=True)
            # print(f"Converted {input_file} to {output_file}")
            # 使用 exiftool 添加 XMP 元数据
            add_xmp_command = ['exiftool', '-overwrite_original', '-xmp:description=compressed', output_file]
            subprocess.run(add_xmp_command, check=True)
            # print(f"Added XMP metadata to {output_file}")
        elif extension in ('.png', '.bmp'):
            # 构建 cwebp 命令
            cwebp_command = ['cwebp', '-q', '50', '-lossless', '-sharp_yuv', input_file, '-o', output_file]
            # 调用 cwebp 命令
            subprocess.run(cwebp_command, check=True)
            # print(f"Converted {input_file} to {output_file}")
            # 使用 exiftool 添加 XMP 元数据
            add_xmp_command = ['exiftool', '-overwrite_original', '-xmp:description=compressed', output_file]
            subprocess.run(add_xmp_command, check=True)
            # print(f"Added XMP metadata to {output_file}")
        else:
            # 其他类型文件，直接复制到输出文件夹
            shutil.copy2(input_file, output_file)
            # print(f"Copied {input_file} to {output_file}")
    #
    except (subprocess.CalledProcessError, IOError) as e:
        print(f"Error processing {input_file}: {e}")
        with open(error_log_file, 'a', encoding='utf-8') as log:
            log.write(f"Error processing {input_file}: {e}\n")


# 遍历文件夹函数
def convert_images(input_dir, output_dir):
    tasks = []
    processed_count = 0
    total_files = sum(len(files) for _, _, files in os.walk(input_dir))

    with ThreadPoolExecutor(max_workers=10) as executor:
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
                    print(f"Processed {processed_count} files out of {total_files} total files")
            except Exception as e:
                continue

# 执行转换或复制
convert_images(input_folder, output_folder)