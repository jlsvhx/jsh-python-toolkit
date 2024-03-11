# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 00:41:54 2022

@author: jshfs
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 23:21:44 2022

@author: jshfs
"""

import os
import shutil
import datetime
    
maindir = r"E:\0_Immortal\IMMO-04 Pics\二次元 Artist"


def checkSecondarDir():
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
                flag = False
                print(tmp)
                
    if(flag):
        print("当前主目录下的每个文件夹中不存在二级子目录")

if __name__ == '__main__': 
    checkSecondarDir()