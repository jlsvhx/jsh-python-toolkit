# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 08:37:20 2024

@author: jshfs
"""

#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
"""显示目录树状图"""
import os

# site存储出现转折的层级号
site = []
lines = []

def not_end_with_exe(item):
    return not item.endswith(".exe")

def write_to_readme():
    with open("readme.txt","w",encoding='utf-8') as f:
        for line in lines:
            f.write(line+"\r\n")

def generate_file_tree_global(path, depth):
    """
    递归打印文件目录树状图（使用全局变量）
    
    :param path: 根目录路径
    :param depth: 根目录、文件所在的层级号
    :return: None
    """
    global site
    filenames_list = os.listdir(path)
    if len(filenames_list) < 1:
        return
    
    filenames_list = list(filter(not_end_with_py,filenames_list))
    # 本级目录最后一个文件名
    last_filename = filenames_list[-1]

    for item in filenames_list:
        string_list = ["│   " for _ in range(depth - site.__len__())]
        for s in site:
            string_list.insert(s, "    ")

        if item != last_filename:
            string_list.append("├── ")
        else:
            # 本级目录最后一个文件名，即为转折处
            string_list.append("└── ")
            # 添加当前出现转折的层级号
            site.append(depth)

        #print("".join(string_list) + item)
        line = "".join(string_list) + item
        print(line)
        lines.append(line)

        new_path = path + '/' + item
        if os.path.isdir(new_path):
            generate_file_tree_global(new_path, depth + 1)
        if item == last_filename:
            # 结束本级目录搜索时，回收（移除）当前的转折层级号
            site.pop()


if __name__ == '__main__':
    # root_path = input("请输入根目录路径：")
    #root_path = r"E:\ProjectXY\ProjectDevFlow\设备监控"
    root_path = os.getcwd()
    #print(os.path.abspath(root_path))
    last_dir = os.path.split(root_path)[-1]
    lines.append(last_dir)
    generate_file_tree_global(root_path, depth=0)
    write_to_readme()
