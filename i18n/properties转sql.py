keyset = set()
def generate_insert_statement(key, zh, en=None, sp=None, ru=None, fr=None):
    insert_statement = "INSERT INTO `i18n` (`wkey`, `zh`) VALUES "
    values = f"('{key}', '{zh}')"
    return insert_statement + values + ";"

def read_properties_file(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('=')
                key = parts[0].strip()
                value = '='.join(parts[1:]).strip()  # 将剩余的部分组合成 value
                data[key] = value
    return data

properties_file_path = "zh.properties"
data = read_properties_file(properties_file_path)

with open('output.sql', 'w', encoding='utf-8') as file:
    for key, value in data.items():
        value = value.replace("'", "''")  # 处理单引号，以防在 SQL 语句中引起问题
        if key not in keyset:
            insert_statement = generate_insert_statement(key, value)
            file.write(insert_statement + '\n')
            keyset.add(key)