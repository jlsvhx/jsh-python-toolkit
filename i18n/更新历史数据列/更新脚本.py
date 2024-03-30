import pandas as pd

# 读取文本文件
with open('keyvalue.txt', 'r',encoding='utf-8') as file:
    lines = file.readlines()

# 解析文本内容为字典
data = {}
for line in lines:
    key, value = line.strip().split('=')
    data[key] = value

# 读取Excel文件
df = pd.read_excel('国际化_更新历史数据列.xlsx')

# 更新Excel中对应行
for key, value in data.items():
    df.loc[df['编号'] == key, '中文（Chinese）'] = value

# 保存更新后的Excel文件
df.to_excel('output.xlsx', index=False)
