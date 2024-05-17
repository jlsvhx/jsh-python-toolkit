import re

# 读取原始文本
with open("替换完code值.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# 提取信息并输出
for line in lines:
    # 使用正则表达式匹配每行中的关键信息
    match = re.match(r'key:(.*?),zh:(.*?),fr:(.*?),en:(.*?),es:(.*?),ru:(.*?)$', line.strip())
    if match:
        key = match.group(1)
        zh = match.group(2)
        en = match.group(4)
        es = match.group(5)
        ru = match.group(6)
        fr = match.group(3)

        # 根据提取的信息生成输出语句
        output = f'INSERT into i18n(wkey,zh,en,es,ru,fr) VALUES("{key}","{zh}","{en}","{es}","{ru}","{fr}");'
        print(output)
