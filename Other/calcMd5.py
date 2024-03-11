# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 12:23:31 2022

@author: jshfs
"""

import sys
import hashlib

import sqlite3

# 连接数据库
connection = sqlite3.connect('model.db')
# 创建游标
cursor = connection.cursor()
#%%

# 创建表
# cursor.execute('''CREATE TABLE IF NOT EXISTS CLASS(
#         ID INT PRIMARY KEY     NOT NULL,
#         NAME           TEXT    NOT NULL,
#         AGE            INT     NOT NULL
#         )''')
 
# Insert操作
md5 = "d71e7c9975203c5013fe1d728b0327aa"
cursor.execute(f"select count(*) from trdModel where md5 = '{md5}'")
exist = cursor.fetchone()
if(exist[0]==0):
    # cursor.execute(f"INSERT INTO trdModel (model,md5,filename) VALUES ('li', '{md5}', 'li1')")
    # connection.commit()
    print()
else:
    cursor.execute(f"SELECT model,md5,filename from trdModel where md5 = '{md5}'")
    connection.commit()
    print("已经存在:   ")
    outcome = cursor.fetchall()
    print(outcome)
    
# 提交当前事务
# connection.commit()
# # Select操作
# cursor.execute("SELECT id,model,md5,filename from trdModel")
# print("fetchone:", cursor.fetchone())
# print("fetchmany:", cursor.fetchmany(2))
# print("fetchall:", cursor.fetchall())
# 关闭数据库连接
connection.close()
