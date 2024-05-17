import re

# 读取原始文本
with open("input.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 读取并构建各语言的映射字典
languages = ["zh", "fr", "en", "es", "ru"]
language_to_text = {}
for language in languages:
    with open(f"{language}.txt", "r", encoding="utf-8") as file:
        language_text = file.read()
        code_to_text = {}
        matches = re.findall(r"'(code\d+)': '(.*?)',", language_text)
        for match in matches:
            code_to_text[match[0]] = match[1]
        language_to_text[language] = code_to_text

# 匹配 i18n.t('codeX')，并替换为对应的文本
matches = re.finditer(r'(\b(?:exception_\d+)\b):\s*i18n\.t\(\'([^\']*)\'\)', text)
for match in matches:
    key = match.group(1)
    code = match.group(2)
    languages_output = []
    for language, code_to_text in language_to_text.items():
        if code in code_to_text:
            if code_to_text[code]:
                languages_output.append(f"{language}:{code_to_text[code]}")
            else:
                languages_output.append(f"{language}:预留")
        else:
            languages_output.append(f"{language}:预留")
    print(f"key:{key}," + ",".join(languages_output))
