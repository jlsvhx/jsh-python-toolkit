# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 00:34:07 2022

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

workdir = r"E:\0_Immortal\IMMO-04 Pics\三次元 Model"
targetdir = r"E:\1_Regenerable\三次元 Model Webp"

def get_file_md5(fname):
    m = hashlib.md5()   #创建md5对象
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  #更新md5对象

    return m.hexdigest()    #返回md5对象

def calcMd5():
    # workdir = r"C:\Users\jshfs\Downloads"

    
    # 连接数据库
    connection = sqlite3.connect('model.db')
    # 创建游标
    cursor = connection.cursor()
    
    for dir in os.listdir(workdir):
        
        md5list = []
        
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
            
            if(os.path.isfile(curfile)):
                curmd5 = get_file_md5(curfile)
                tmp = [str(dir),str(file),str(curmd5)]
                md5list.append(tmp)
                
                
            else:
                print(curdir + "存在子文件夹:" + file)
    
        for line in md5list:
            cmodel = line[0]
            cname = line[1]
            cmd5 = line[2]
    
            cursor.execute(f"select * from trdModel where md5 == '{cmd5}'")
            exist = cursor.fetchone()
            # print(exist)
            if exist is None:
                cursor.execute(f"INSERT INTO trdModel (model,md5,filename) VALUES ('{cmodel}', '{cmd5}', '{cname}')")

            else:
                print(cname)
                print(exist)
                # cursor.execute(f"SELECT model,md5,filename from trdModel where md5 = '{cmd5}'")
                # outcome = cursor.fetchall()
                # print(outcome)
    
   
    
    connection.commit()
    # 关闭数据库连接
    connection.close()
    

    # file_name='md5.txt'
    # with open(file_name, 'w', encoding='utf-8') as can:
    #     for md5 in md5list:
    #         can.write(md5+"\n")