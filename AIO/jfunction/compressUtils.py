# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 00:41:04 2022

@author: jshfs
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:09:27 2022

@author: jshfs
"""
import sqlite3
from ffmpy3 import FFmpeg # pip install ffmpy3
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




def png2webpV1(sourceDir,targetDir):
    
    # 计数变量
    count = 0
    
    # subFolderName 为源文件夹下的文件列表
    for subFolderName in os.listdir(sourceDir):
        
        # sourceSubFolderFullPath 为源文件夹下的子文件夹的全路径
        sourceSubFolderFullPath = os.path.join(sourceDir,subFolderName)
        
        # sourceSubFolderFullPath 如果不是文件夹，则跳过
        if(not os.path.isdir(sourceSubFolderFullPath)):
            continue
        
        print(sourceSubFolderFullPath)
        
        # targetSubFolderFullPath 为目标文件夹下的子文件夹的全路径
        targetSubFolderFullPath = os.path.join(targetDir,subFolderName)
        
        # targetSubFolderFullPath 不存在则创建
        if(not os.path.exists(targetSubFolderFullPath)):
            os.mkdir(targetSubFolderFullPath)
        
        for file in os.listdir(sourceSubFolderFullPath):
            
            count = count + 1
            
            curfile = os.path.join(sourceSubFolderFullPath,file)
            fileName = os.path.splitext(file)[0]
            
            outWebpFile = os.path.join(targetSubFolderFullPath,fileName+".webp") # 目标webp文件
            outSameNameFile = os.path.join(targetSubFolderFullPath,file) # 目标同名文件，即非可转换文件
            
            if(os.path.isdir(curfile) or os.path.exists(outWebpFile) or os.path.exists(outSameNameFile)): 
                count = count -1
                # 如果目标文件已存在则跳过
                continue
            
            if(os.path.isfile(curfile)):
                if(curfile.endswith(('.mp4', '.mkv', '.avi', '.wmv', '.iso', '.mov', '.pdf','.m4v','.txt','.webm'))):
                    # 如果非图像文件，则直接复制过去即可
                    if(not os.path.exists(outSameNameFile)):
                        copyfile(curfile,outSameNameFile)
                       
                elif(os.path.getsize(curfile)>1024*1024*15): # 源文件大于15MB则采用75的压缩质量
                    try: # 尝试转换为webp
                        ff = FFmpeg(inputs={curfile: None},
                        outputs={outWebpFile: '-codec libwebp -lossless 0 -quality 75'})
                        print(ff.cmd)
                        ff.run()
                    except : # 不能转换时，直接复制原文件
                        copyfile(curfile,outSameNameFile)
                
                elif(os.path.getsize(curfile)>1024*1024*10): # 源文件大于10MB则采用80的压缩质量
                    try: # 尝试转换为webp
                        ff = FFmpeg(inputs={curfile: None},
                        outputs={outWebpFile: '-codec libwebp -lossless 0 -quality 80'})
                        print(ff.cmd)
                        ff.run()
                    except : # 不能转换时，直接复制原文件
                        copyfile(curfile,outSameNameFile)
                        
                elif(os.path.getsize(curfile)>1024*1024*5): # 源文件大于5MB则采用85的压缩质量
                    try: # 尝试转换为webp
                        ff = FFmpeg(inputs={curfile: None},
                        outputs={outWebpFile: '-codec libwebp -lossless 0 -quality 85'})
                        print(ff.cmd)
                        ff.run()
                    except : # 不能转换时，直接复制原文件
                        copyfile(curfile,outSameNameFile)
                        
                elif(os.path.getsize(curfile)>1024*1024): # 源文件大于1MB则采用90的压缩质量
                    try:
                        ff = FFmpeg(inputs={curfile: None},
                        outputs={outWebpFile: '-codec libwebp -lossless 0 -quality 90'})
                        print(ff.cmd)
                        ff.run()
                    except :
                        copyfile(curfile,outSameNameFile)
                        
                else: # 源文件小于1MB则直接复制原文件
                    copyfile(curfile,outSameNameFile)
                    
            else:
                print(sourceSubFolderFullPath + "存在子文件夹:" + file)
                
        # 从目标子文件夹中删除多余的文件
        targetFileList = os.listdir(targetSubFolderFullPath)
        targetFileDict = getDict(targetFileList)
        
        sourceFileList = os.listdir(sourceSubFolderFullPath)
        sourceFileSet = getSet(sourceFileList)
        
        for k in list(targetFileDict.keys()):
            if k in sourceFileSet:
                # print(k)
                del targetFileDict[k]
                
        for k in list(targetFileDict.keys()):
            t = targetFileDict[k]
            tmp = os.path.join(targetSubFolderFullPath,t)
            # 
            print(tmp)
            os.remove(tmp)
        
        
        print("s")
        
        
    print(f'本次压缩处理{count}张照片')

def fileListRemoveSuffix(listList):
    for i in range(len(listList)):
        listList[i]=os.path.splitext(listList[i])[0]
        
def getSet(listList):
    res = set()
    for i in range(len(listList)):
        t=os.path.splitext(listList[i])[0]
        res.add(t)
    return res
        
def getDict(listList):
    res = {}
    for i in range(len(listList)):
        t=os.path.splitext(listList[i])[0]
        res[t]=listList[i]
    return res
    
