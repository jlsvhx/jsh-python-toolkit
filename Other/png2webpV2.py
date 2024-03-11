# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:09:27 2022

@author: jshfs
"""
import sqlite3
from ffmpy3 import FFmpeg
import os
from shutil import copyfile
import hashlib
import subprocess
import glob
import json
import shlex
import time
import re
from os import path
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
from pprint import pprint

workdir = r"E:\0_Immortal\IMMO-04 Pics\二次元 Artist"
targetdir = r"E:\1_Regenerable\二次元 Artist Webp"


def png2webpV2():
    """
    采用magick的命令行进行转换操作，能使用一些Imagemagick的特性
    
    """
    count = 0
    for dir in os.listdir(workdir):
        
        curdir = os.path.join(workdir,dir)
        if(not os.path.isdir(curdir)):
            continue
        
        print(curdir)
        curTdir = os.path.join(targetdir,dir)
        if(not os.path.exists(curTdir)):
            os.mkdir(curTdir)
        
        for file in os.listdir(curdir):
            
            curfile = os.path.join(curdir,file)
            fileName = os.path.splitext(file)[0]
            outFile = os.path.join(curTdir,fileName+".jpg") # 目标webp文件
            outSameNameFile = os.path.join(curTdir,file) # 目标同名文件，即非可转换文件
            
            if(os.path.isdir(curfile) or os.path.exists(outFile) or os.path.exists(outSameNameFile)): 
                # 如果目标文件已存在则跳过
                continue
            count = count + 1
            if(os.path.isfile(curfile)):
                if(curfile.lower().endswith(('.mp4', '.mkv', '.avi', '.wmv', '.iso', '.mov', '.pdf','.m4v','.txt','.gif','.webm'))):
                    # 如果非图像文件，则直接复制过去即可
                   if(not os.path.exists(outSameNameFile)):
                       copyfile(curfile,outSameNameFile)
                       
                elif(os.path.getsize(curfile)>1024*1024*15): 
                    subprocess.run(
                        shlex.split(f'magick convert "{curfile}" -quality 65 "{outFile}"'
                        ), capture_output=True)
                    压缩比率=int(os.path.getsize(curfile)/os.path.getsize(outFile))
                    print(f"压缩比率={压缩比率}, {curfile}")
# =============================================================================
#                     宽高比 = subprocess.run(shlex.split(f'magick identify -format "%[fx:w/h]" "{curfile}"'),capture_output=True).stdout
#                     print(宽高比)
#                     
#                     details = subprocess.run(shlex.split(f'magick identify -verbose "{curfile}"'),capture_output=True).stdout
#                     print(type(details))
#                     details = str(details, 'UTF-8')
#                     details = details.split("\n")
#                     for line in details:
#                         if(line.strip().startswith("Number")):
#                             num = line.split()[2]
#                             if(num.endswith("M")):
#                                 num = num[0:-1]
#                                 num = int(num)
#                                 print(num*1000000)
#                             else:
#                                 num = int(num)
#                                 print(num)
#                                 
#                     numberOfpixels = 12000000
# =============================================================================
                elif(os.path.getsize(curfile)>1024*1024*10):
                    subprocess.run(
                        shlex.split(f'magick convert "{curfile}" -quality 70 "{outFile}"'
                        ), capture_output=True)
                    压缩比率=int(os.path.getsize(curfile)/os.path.getsize(outFile))
                    print(f"压缩比率={压缩比率}, {curfile}")
                    
                elif(os.path.getsize(curfile)>1024*1024*5):
                    subprocess.run(
                        shlex.split(f'magick convert "{curfile}" -quality 75 "{outFile}"'
                        ), capture_output=True)
                    压缩比率=int(os.path.getsize(curfile)/os.path.getsize(outFile))
                    print(f"压缩比率={压缩比率}, {curfile}")
                    
                elif(os.path.getsize(curfile)>1024*1024):
                    subprocess.run(
                        shlex.split(f'magick convert "{curfile}" -quality 80 "{outFile}"'
                        ), capture_output=True)
                    压缩比率=int(os.path.getsize(curfile)/os.path.getsize(outFile))
                    print(f"压缩比率={压缩比率}, {curfile}")
                    
                else: # 源文件小于1MB则直接复制原文件
                    copyfile(curfile,outSameNameFile)

                    
            else:
                print(curdir + "存在子文件夹:" + file)
    print(f'本次压缩处理{count}张照片')



if __name__ == '__main__': 
    png2webpV2()