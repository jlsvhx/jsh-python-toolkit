import os

import pandas as pd

"""
Created on Mon Jul 22 14:
@author: <JSH>
"""


"""
    从告警config.js中提取异常信息并编号，将编号回写到config.js中
"""


def extractors():
    import re
    from openpyxl import Workbook

    # 文本内容
    with open("config.txt", "r", encoding='utf-8') as file:
        text = file.read()

    text = """
    const NEW_DQDXT = {      //报警  modified by yxl 20230704
    alarm_1:	'新平台',
      alarm_65:	'低湿报警',
    """

    # 文本内容
    with open("config.txt", "r", encoding='utf-8') as file:
        text = file.read()

    # 提取异常信息
    # old_exceptions = re.findall(r"(exception|alarm)_(\d+): '(.+)'", text)
    old_exceptions = re.findall(r"(exception|alarm)_(\d+):\s*'(.+?)'", text)

    # 创建Excel工作簿和工作表
    wb = Workbook()
    ws = wb.active

    # 写入标题行
    ws.append(["类型", "编号", "异常信息"])

    # 使用集合来存储已经出现过的异常信息
    seen_exceptions = {}

    # 写入异常信息
    for idx, exception in enumerate(old_exceptions, start=1):
        # 检查异常信息是否已经存在，如果不存在则写入Excel文件
        if exception[2] not in seen_exceptions:
            code = 'code' + str(idx)
            ws.append([exception[0], code, exception[2]])
            seen_exceptions[exception[2]] = code

    # 替换文本中的异常信息为带有编号的异常信息
    for key, value in seen_exceptions.items():
        text = text.replace(f"'{key}'", f"'{value}'")

    # 将带有编号的异常信息写回到原文件中
    with open("output.txt", "w", encoding='utf-8') as file:
        file.write(text)

    # 保存Excel文件
    wb.save("异常信息.xlsx")


def chinese2eng():
    import pandas as pd
    import re

    # 读取 Excel 文件
    df = pd.read_excel("eng.xlsx")

    # 将中文列作为键，英文列作为值存入字典中
    translation_dict = dict(zip(df['中文'], df['英文']))

    # 读取文本文件内容
    with open("eng.txt", "r", encoding='utf-8') as file:
        text = file.read()

    # 逐个替换文本中的中文内容
    for chinese_text, english_translation in translation_dict.items():
        # 构造要替换的字符串
        pattern = f"'{chinese_text}'"
        replacement = f"'{english_translation}'"
        # 替换文本中的内容
        text = re.sub(pattern, replacement, text)

    # 将替换后的文本内容写回到原文件中
    with open("eng.txt", "w", encoding='utf-8') as file:
        file.write(text)

import pandas as pd

import pandas as pd

def calculate_chinese_length(text):
    if isinstance(text, str):
        if len(text)*2 <= 10:
            return 10
        else:
            return len(text)*2
    return ""

def process_excel_file(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 获取 '中文字段' 列
    chinese_column = df['中文字段']

    # 计算每行的中文字符长度，每个中文字符长度算作1
    chinese_length = chinese_column.apply(calculate_chinese_length)

    # 将计算结果写入到 '标签翻译后最大长度' 列中
    df['标签翻译后最大长度'] = chinese_length

    # 保存修改后的 DataFrame 到原 Excel 文件
    df.to_excel(file_path, index=False)

    print(f"计算结果已写入到原 Excel 文件的'标签翻译后最大长度'列中。")

def addi18nt():
    import re

    # 读取 config.js 文件
    with open('config.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # 定义一个模拟的i18n.t函数
    def i18n_t(text):
        return f"i18n.t('{text}')"

    # 定义需要排除的预留字样
    reserved_keywords = ['i18n.t']

    # 定义替换函数
    def replace(match):
        if match.group(1) not in reserved_keywords:
            return i18n_t(match.group(1))
        else:
            return match.group(0)

    # 匹配单引号包含的内容并加上i18n.t
    content = re.sub(r"'([^']*)'", replace, content)

    # 将处理后的内容写入 config2.js 文件
    with open('config2.js', 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    process_excel_file('待翻译2.xlsx')
