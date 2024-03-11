# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 16:23:47 2022

@author: jshfs
"""
from pypinyin import pinyin, lazy_pinyin, Style
import os
import json

from functools import cmp_to_key
def cmp(t1, t2):
    """
    比较函数，需要满足：t1>t2则返回正数，t1=t0则返回0，t1<t2则返回负数。
    """
    board = min(len(t1),len(t2))
    for i in range(0,board):
        if ord(t1[i]) != ord(t2[i]):
            return ord(t1[i]) - ord(t2[i])
    return len(t1) - len(t2)


def pinyinSort(stringlist):
    stringlist = sorted(stringlist)
    anslist = []
    pairDict = {}
    idx = 0
    while idx < len(stringlist):
        
        string = stringlist[idx]
        # print(str(idx)+":"+string)
        firstChar = string[0]
        if not '\u4e00' <= firstChar <= '\u9fa5':
            anslist.append(string)
        else:
            break
        idx = idx + 1
    # print(idx)
    for i in range(idx,len(stringlist)):
        string = stringlist[i]
        # print(string)
        tmplist = pinyin(string, style=Style.FIRST_LETTER)
        sortedkey = ''
        for _tmp in tmplist:
            sortedkey = sortedkey + str(_tmp)
        pairDict[sortedkey]=string
    for k in sorted(pairDict):
        anslist.append(pairDict[k])
    return anslist
    

tardir = r"E:\anti-disaster backup\坚果云\深海剪藏\三次元 Model Record"

# tardir = r"三次元.md"
# tardir = r"test.md"

for cfile in os.listdir(tardir):
    if(cfile.endswith("txt")):
        
        filelist = []
        name = ""
        data = {}
        
        # import shutil
        
        # source = '三次元.md'
        # target = 'last三次元.md'
        
        # # create the folders if not already exists
        # # os.makedirs(target)
        
        # # adding exception handling
        # shutil.copy(source, target)
        
           
        
        with open(os.path.join(tardir,cfile),'r',encoding='UTF-8') as f:
            lines = f.readlines()
            lines = [i.strip() for i in lines]
            for line in lines:
                if (len(line)!=0):
                    # cur = line
                    # idx = 0
                    # while idx<len(cur) and cur[idx]!='.':
                    #     idx = idx + 1
                    # filelist.append(cur[idx+2:])
                    filelist.append(line)
                else :
                    continue
                
        # with open(os.path.join(tardir,cfile),'r',encoding='UTF-8') as f:
        #     lines = f.readlines()
        #     lines = [i.strip() for i in lines]
        #     for line in lines:
        #         if(line.startswith("#")):
        #             name = line[3:]
        #             data[name]=[]
        #             # print(name)
        #         elif (len(line)!=0):
        #             data[name].append(line)
        #         else :
        #             continue
        
        
            # for _char in key:
            #     if '\u4e00' <= _char <= '\u9fa5':
            #         tmp = tmp + _char
            #     else:
        filelist = pinyinSort(filelist)
        # for i,sub in  enumerate(filelist):
        #     print(str(i)+'. '+sub+"\n")
        with open(os.path.join(tardir,cfile),'w',encoding='UTF-8') as f:
            for i,sub in  enumerate(filelist):
                # f.write(str(i)+'. '+sub+"\n")
                f.write(sub+"\n")
            
        # with open("三次元.md","w",encoding='utf-8') as f:
        #     for key in sortedkeys:
        #         f.write("## "+key+"\r\n")
        #         filelist = data[key]
        #         for i in range(0,len(filelist)):
        #             # print(filelist[i])
        #             cur = filelist[i]
        #             idx = 0
        #             while idx<len(cur) and cur[idx]!='.':
        #                 idx = idx + 1
        #             filelist[i]=filelist[i][idx+2:]
        #         filelist = sorted(filelist)
                
        #         for i,sub in  enumerate(filelist):
        #             # single = str(i)+'. '+sub[2:]+"\r\n"
        #             # print(single)
        #             # print(sub)
        #             f.write(str(i)+'. '+sub+"\n")
# with open("record.json","w") as f:
#     json.dump(data,f)
#     print("加载入文件完成...")
    
# with open("record.json",'r') as load_f:
#     load_dict = json.load(load_f)
#     print(load_dict)