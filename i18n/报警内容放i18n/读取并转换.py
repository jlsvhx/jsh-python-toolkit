import re

# 读取文本文件
with open("原始config.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 使用正则表达式匹配每个 const 开头的文本
matches = re.finditer(r'const\s+(\w+)\s+=\s+\{(?:.*?\n)*?\}', text)

# 遍历每个匹配项
for match in matches:
    const_name = match.group(1)  # 获取 const 后面的名称
    const_content = match.group(0)  # 获取 const 的内容

    # 使用正则表达式替换 const 内的 alarm
    const_content = re.sub(r'\balarm', f'{const_name}', const_content)

    # 替换原文本中的 const 内容
    text = text.replace(match.group(0), const_content)

# 写回文本文件
with open("替换成机型名的config.txt", "w", encoding="utf-8") as file:
    file.write(text)
