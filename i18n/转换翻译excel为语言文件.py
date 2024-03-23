import os

import pandas as pd

"""
Created on Mon Jul 22 14:
@author: <JSH>
"""

"""
    读取翻译好的excel文件，将excel文件转化为'编号'：'翻译'的键值对，可以直接复制到 语言.js 中使用
"""


def read_excel(filename):
    sheet_names = pd.ExcelFile(filename).sheet_names
    for sheet_name in sheet_names:

        df = pd.read_excel(filename, sheet_name=sheet_name)

        # 获取列名
        column_names = df.columns.tolist()

        for column_name in column_names:
            if column_name == '编号':
                continue
            else:

                # 删除包含空值的行
                df = df.dropna(subset=['编号', column_name])

                # 将数据转换为字典
                exceptions_dict = df.set_index('编号')[column_name].to_dict()

                # 将字典内容写入文本文件
                with open(sheet_name+column_name + ".txt", "w", encoding='utf-8') as file:
                    for key, value in exceptions_dict.items():
                        if key == 'nan':
                            continue
                        file.write(f"'{key}': '{value}',\n")


if __name__ == '__main__':
    read_excel("fin_excel/历史曲线标签20240322.xlsx")
