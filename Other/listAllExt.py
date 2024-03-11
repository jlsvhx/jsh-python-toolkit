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


def listAllExt():
    """
    
    """
    extlist = set()
    for root, dirs, files in os.walk(maindir):
        for file in files:
            ext = os.path.splitext(file)[-1]
            extlist.add(ext)
    print(extlist)

if __name__ == '__main__': 
    listAllExt()