import logging
from faker import Faker
import csv

fake = Faker('zh_CN')

names = [fake.name() for _ in range(100)]

# 写入到 ./data/names.csv 文件
with open('./data/names.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['姓名'])  # 表头
    for name in names:
        writer.writerow([name])
        
if __name__ == '__main__':
    pass
