import os
import hashlib
import sqlite3
import datetime
from threading import Thread
from queue import Queue, Empty
from tkinter import Tk, filedialog
from tqdm import tqdm

# 计算文件的MD5值
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# 获取文件的最后修改时间
def get_file_modification_time(file_path):
    mod_time = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(mod_time)

# 初始化数据库
def initialize_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS files_md5 (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_path TEXT NOT NULL,
                        md5 TEXT NOT NULL,
                        modification_time TEXT NOT NULL
                      )''')
    # 在 file_path 列上创建索引
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_file_path ON files_md5 (file_path)''')
    conn.commit()
    conn.close()

db_name = 'file_integrity_check.db'
exclude_file_names = [db_name]

def push_files_to_process(main_directory, task_queue):
    for root, dirs, files in os.walk(main_directory):
        for file in files:
            if file in exclude_file_names or file.endswith('.sfv'):
                continue
            task_queue.put(os.path.join(root, file))

# 验证文件MD5值和修改时间
def verify_md5_in_folder(main_directory, thread_count=4):
    task_queue = Queue()
    result_queue = Queue()

    db_path = os.path.join(main_directory, db_name)
    initialize_db(db_path)

    push_files_to_process(main_directory, task_queue)
    total_files = task_queue.qsize()

    def worker(pbar):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        while not task_queue.empty():
            try:
                file_path = task_queue.get_nowait()
                current_md5 = calculate_md5(file_path)
                current_mod_time = get_file_modification_time(file_path)
                relative_path = os.path.relpath(file_path, main_directory)

                cursor.execute('SELECT md5, modification_time FROM files_md5 WHERE file_path = ?', (relative_path,))
                result = cursor.fetchone()

                if result is None:
                    result_queue.put((file_path, True, "未找到对应的MD5记录，已添加"))
                    cursor.execute('INSERT INTO files_md5 (file_path, md5, modification_time) VALUES (?, ?, ?)',
                                   (relative_path, current_md5, current_mod_time))
                    conn.commit()
                else:
                    db_md5, db_mod_time_str = result
                    db_mod_time = datetime.datetime.fromisoformat(db_mod_time_str)

                    if current_mod_time == db_mod_time:
                        if current_md5 == db_md5:
                            result_queue.put((file_path, True, "MD5与数据库一致"))
                        else:
                            result_queue.put((file_path, False, "文件损坏"))
                    else:
                        cursor.execute('UPDATE files_md5 SET md5 = ?, modification_time = ? WHERE file_path = ?',
                                       (current_md5, current_mod_time, relative_path))
                        conn.commit()
                        result_queue.put((file_path, False, "文件已修改，MD5已更新"))
            except Empty:
                break
            finally:
                pbar.update(1)

        conn.close()

    with tqdm(total=total_files, desc="Processing files") as pbar:
        threads = []
        for _ in range(thread_count):
            thread = Thread(target=worker, args=(pbar,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    while not result_queue.empty():
        file_path, success, message = result_queue.get()
        if success:
            # print(f"文件 {file_path} 验证成功: {message}")
            pass
        else:
            print(f"文件 {file_path} 验证失败: {message}")

    print("\n**MD5计算和验证任务完成**\n")

# 通过文件浏览器选择文件夹
def select_folder():
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    folder_selected = filedialog.askdirectory()
    return folder_selected

if __name__ == '__main__':
    # 示例文件夹路径
    d = select_folder()
    # 验证文件MD5值和修改时间
    verify_md5_in_folder(d, 4)
    input("Press Enter to exit...")
