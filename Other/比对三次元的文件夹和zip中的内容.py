# -*- coding: utf-8 -*-
"""
Created on Wed May  4 20:10:15 2022

@author: jshfs
"""
import zipfile38 as zipfile
import os
from tqdm import tqdm
import subprocess
import shlex

def get_zipfile_namelist(srcfile):
    output_namelist = []
    with zipfile.ZipFile(srcfile, 'r') as zfile:
        for i in zfile.namelist():
            try:
                i=i.encode('cp437').decode('gbk')
            except:
                pass
            output_namelist.append(i)
    return output_namelist


dirpath = r"D:\0_Immortal\IMMO-04 Pics\二次元 Artist"
zippath = r"E:\0_Immortal\IMMO-04 Pics\二次元 Artist"

n = len(os.listdir(dirpath))
pbar = tqdm(total=n)

for k,dir in enumerate(os.listdir(dirpath)):
    
    pbar.update(1)
    
    curdir = os.path.join(dirpath,dir)
    
    if(not os.path.isdir(curdir)):
        continue
    
    dirfilelist = os.listdir(curdir)
    
    curzip = os.path.join(zippath,dir)+".zip"
    if(not os.path.exists(curzip)):
        tqdm.write(dir+"不存在")
        try:
            tqdm.write(dir+"压缩中")
            subprocess.run(
                shlex.split(f'zip -j "{curzip}" "{curdir}/*"')
                , capture_output=True)
            tqdm.write(dir+"压缩完成\n")
        except:
            pass
    else:
        zipfilelist = get_zipfile_namelist(curzip)
        if(dirfilelist != zipfilelist):
            tqdm.write(dir + " 需要重新压缩")
            try:
                os.remove(curzip)
                tqdm.write(dir+"压缩中")
                subprocess.run(
                    shlex.split(f'zip -j -1 "{curzip}" "{curdir}/*"')
                    , capture_output=True)
                tqdm.write(dir+"压缩完成\n")
            except:
                pass

pbar.close()
