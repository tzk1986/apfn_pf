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
        
def generate_test_data(filename, count=100, start_index=1):
    fake = Faker('zh_CN')
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['昵称', '手机号', '工号', '部门', '职务'])
        for i in range(start_index, start_index + count):
            nickname = fake.name()
            mobile = ''
            job_id = f"zfcs{i:07d}"
            department = '产品部7'
            position = '产品'
            writer.writerow([nickname, mobile, job_id, department, position])

if __name__ == '__main__':
    # 例如已生成100条，下次从101开始
    generate_test_data('./data/test_users1226001.csv', count=100, start_index=1)
        

