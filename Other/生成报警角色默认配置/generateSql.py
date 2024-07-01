import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('config1.xlsx')

# 定义插入语句的模板
insert_template = """
INSERT INTO device_alarm_role_config (role_id, alarm_id, location_type, delay_time, ring, receive)
VALUES ({role_id}, {alarm_id}, {location_type}, {delay_time}, {ring}, {receive});
"""

# 生成插入语句
insert_statements = []
for index, row in df.iterrows():
    insert_statement = insert_template.format(
        role_id=row['role_id'],
        alarm_id=row['alarm_id'],
        location_type=row['location_type'],
        delay_time=row['delay_time'],
        ring=row['ring'],
        receive=row['receive']
    )
    insert_statements.append(insert_statement)

# 将插入语句写入到文件
with open('config1.txt', 'w', encoding='utf-8') as file:
    for statement in insert_statements:
        file.write(statement + '\n')

print("SQL insert statements have been written to output.txt")