# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 00:22:36 2022

@author: jshfs
"""
import os
import shutil
import datetime
    
maindir = r"E:\0_Immortal\IMMO-04 Pics\三次元 Model"

def deleteSecondarDir():
    """
    查询maindir下的每个文件夹里面，是否有二级子目录
    """
    flag = True
    for dir in os.listdir(maindir):
    
        curdir = os.path.join(maindir,dir)
        
        if(not os.path.isdir(curdir)):
            continue

        for file in os.listdir(curdir):
            tmp = os.path.join(curdir,file)
            if(os.path.isdir(tmp)):
                try:
                    # os.rmdir(tmp)
                    shutil.rmtree(tmp)
                except Exception as err:
                    print(str(err))
                


if __name__ == '__main__': 
    deleteSecondarDir()