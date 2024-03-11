# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 20:51:51 2022

@author: jshfs
"""

import os

tardir = "E:\\"

filelist = os.listdir(tardir)


# import module
import os

def getdirsize(Folderpath):
    # print(Folderpath)
    # assign size
    size = 0
    
    # get size
    for path, dirs, files in os.walk(Folderpath):
    	for f in files:
    		fp = os.path.join(path, f)
    		size += os.path.getsize(fp)
            
    
    # display size
    # print("Folder size: " + str(size))
    return size/1024/1024/1024
    
for file in filelist:
    pathsize = getdirsize(os.path.join(tardir, file))
    print(file+":"+str(pathsize).split('.')[0]+"G")

 # 拼接百度云连接
# for file in filelist:
#     if file.endswith("txt"):
#         with open(os.path.join(tardir,file),"r",encoding='utf-8') as f:
#             line = f.readline()
#             # print(line[3:].strip())
#             line2 = f.readline()
#             line2 = f.readline()
#             # print(line2[4:].strip())
#             print(line[3:].strip()+'?pwd='+line2[4:].strip())

# 提取福利姬txt中的文件名
# tarfile = '福利姬.txt'
# with open(tarfile,'r',encoding='UTF-8') as f:
#     lines = f.readlines()
#     lines = [i.strip() for i in lines]
#     data = {}
#     lastname = ''
#     for i in range(0,len(lines)):
#         cur = lines[i]
#         for j in range(0,len(cur)):
#             if(cur[j]=='/'):
#                 break
#         name = cur[0:j]
#         # print(name)
#         idx = 0
#         while idx+3 < len(cur):
#             if cur[idx:idx+4]=='.zip':
#                 break
#             else:
#                 idx = idx + 1
#         lines[i]=lines[i][j+1:idx]
#         # print(lines[i])
#         if name in data:
#             data[name].append(lines[i])
#         else:
#             data[name]=[]
#             data[name].append(lines[i])
#         # print(lines[i])
        
#     with open("fuli.txt","w",encoding='utf-8') as f:
#         keylist = data.keys()
#         for key in keylist:
#             _filelist = data[key]
#             # f.write(key+"\n")
#             for i,sub in  enumerate(_filelist):
#                 # single = str(i)+'. '+sub[2:]+"\r\n"
#                 # print(single)
#                 # print(sub)
#                 f.write(sub+"\n")

