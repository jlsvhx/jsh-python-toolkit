# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 23:21:44 2022

@author: jshfs
"""

import os
import shutil
import datetime
import imghdr
import tkinter as tk
from tkinter import filedialog

def sub2main():
    
    prefix = os.path.split(maindir)[-1]
    
    seq = 1
    
    for root, dirs, files in os.walk(maindir):
        
        for file in files:
            
            src = os.path.join(root,file)
            
            if(root!=maindir):
                
                oldext = os.path.splitext(file)[1]
                newname = prefix + "_" + str(seq) + oldext
                seq = seq + 1
                
                dst = os.path.join(root,newname)
                print(dst)
                
                try:
                    os.rename(src,dst)
                    print("rename "+src)
                except:
                    print("rename Error!")
            
                try:
                    shutil.move(dst,maindir)
                except:
                    print("move Error!")


def delBlankSubDir():

    for root, dirs, files in os.walk(maindir):
        for seconDir in dirs:
            wholePath = os.path.join(root,seconDir)
            if(len(os.listdir(wholePath))==0):
                shutil.rmtree(wholePath)
                print(wholePath)

                    
if __name__ == '__main__': 

     
    root = tk.Tk()
    root.withdraw() # 隐藏主窗口
    
    global maindir
    maindir = filedialog.askdirectory(title='选择文件夹')
    
    print("所选的文件夹路径为：", maindir)
    sub2main()
    delBlankSubDir()