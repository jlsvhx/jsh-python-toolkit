# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 20:37:39 2022

@author: jshfs
"""

import os
import shutil

workdir = r"E:\写真\tmp"

def moveTxt2samenameFolder():
    # 将workdir下的txt放到同名目录下
    for dir in os.listdir(workdir):
        
        
        if(dir.endswith("txt") and os.path.exists(os.path.join(workdir,dir[0:-4]))):
            src = os.path.join(workdir,dir)
            dst = os.path.join(workdir,dir[0:-4],dir)
            # print(f"shutil.move({src},{dst})")
            try:
                shutil.move(src,dst)
            except:
                print("move Error!")
        
def averageMove():

    dirlist = os.listdir(workdir)
    count = 0
    folderIndex = 0
    for dir in dirlist:
        if(count>23):
            count = 0
            folderIndex = folderIndex + 1
            os.mkdir(os.path.join(workdir,str(folderIndex)))
        count = count + 1
        src = os.path.join(workdir,dir)
        dst = os.path.join(workdir,str(folderIndex),dir)
        try:
            # print(f"{src}==>{dst}")
            shutil.move(src,dst)
        except:
            print("move Error!")
    

if __name__ == '__main__': 
    averageMove()