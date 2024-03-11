# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 23:21:44 2022

@author: jshfs
"""

import os
import shutil
import datetime
import imghdr




def sub2main(maindir):
    """
    将maindir下的每一个目录作为主目录，对主目录下的所有文件重命名，同时提取到主目录下（从所有级子目录中）
    """
    for dir in os.listdir(maindir):
        
        prefix = dir
        curdir = os.path.join(maindir,dir)
        
        if(not os.path.isdir(curdir)):
            continue
        
        seq = 1
        
        for root, dirs, files in os.walk(curdir):
            
            for file in files:
                
                src = os.path.join(root,file)
                
                if(root!=curdir):
                    
                    oldext = os.path.splitext(file)[1]
                    newname = prefix + "_" +str(datetime.date.today())+ str(seq) + oldext
                    seq = seq + 1
                    
                    dst = os.path.join(root,newname)
                    
                    try:
                        os.rename(src,dst)
                        print("rename "+src)
                    except:
                        print("rename Error!")
                
                    try:
                        # print(f"move {dst}")
                        shutil.move(dst,curdir)
                    except:
                        print("move Error!")
                        
                # else:
                    
                #     check = imghdr.what(src)
                #     if check==None:
                #         print(src+" broken")

def delBlankSubDir(maindir):
    ext = {}
    """
    将maindir下的每一个目录作为主目录，删除主目录下面的空次级目录
    """
    for dir in os.listdir(maindir):
        
        prefix = dir
        curdir = os.path.join(maindir,dir)
        
        if(not os.path.isdir(curdir)):
            continue

        
        for root, dirs, files in os.walk(curdir):
            for seconDir in dirs:
                wholePath = os.path.join(root,seconDir)
                if(len(os.listdir(wholePath))==0):
                    shutil.rmtree(wholePath)
                    print(wholePath)


def queryExt(folder_path):

    ext = set()
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            image_path = os.path.join(root, filename)
            # 获取文件后缀名
            file_name, file_ext = os.path.splitext(filename)
            file_ext = file_ext.lower()
            # 检查文件是否是图像格式
            if file_ext in ext:
                continue
            else:
                ext.add(file_ext)
    print(ext)

if __name__ == '__main__':

    maindir = r"D:\0_Immortal\IMMO-04 Pics\2次元 Artists"
    # sub2main(maindir)
    # delBlankSubDir(maindir)
    # queryExt(maindir)
