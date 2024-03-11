# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 13:12:53 2022

@author: jshfs
"""

import os

tardir = r"E:\0_Immortal\IMMO_04 PI\三次元\三次元.md"

name = ""
data = {}

with open(tardir,'r',encoding='UTF-8') as f:
    lines = f.readlines()
    lines = [i.strip() for i in lines]
    for line in lines:
        if(line.startswith("#")):
            name = line[3:]
            data[name]=[]
            print(name)
        elif (len(line)!=0):
            data[name].append(line)
        else :
            continue
        
keylist = sorted(data)

with open("test.md","w",encoding='utf-8') as f:
    for key in keylist:
        f.write("## "+key+"\r\n")
        filelist = sorted(data[key])
        for sub in data[key]:
            f.write(sub+"\r\n")
            
