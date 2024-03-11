# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 01:17:32 2022

@author: MATX
"""

import os
import json

tardir = r"C:\Users\MATX\Desktop\sql.txt"

name = ""
data = {}


with open(tardir,'r',encoding='UTF-8') as f:
    lines = f.readlines()
    lines = [i.strip() for i in lines]
    k = len(lines)
    print(k)
    i = 0
    flag = False
    
    while(i<k):
        line = lines[i]
        idx = line
        result = lines[i+3]
        
        text = json.loads(result)
        # print(text)
        
        l = len(text["gSB_LIST"])
        for ii in range(l):
            if(not "type" in text["gSB_LIST"][ii]):
                flag = True
                print(idx)
                text["gSB_LIST"][ii]["type"] = 0
        result = json.dumps(text,ensure_ascii=False)
        # if(flag):
        #     print(result)
        
        tmp = "UPDATE suggest_alg_result set result = '"+result+"' where id="+idx+";"
        print(tmp)
        # print(idx)
        flag = False
        print()
        i = i+7
    