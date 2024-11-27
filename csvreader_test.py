from locust_plugins.csvreader import CSVDictReader
import queue

# 创建队列存储数据
q = queue.Queue()

# 读取CSV文件并将数据放入队列
csv_data = CSVDictReader(file="./data/20241126 copy.csv")

user_data = next(csv_data)
print(user_data)


# from locust_plugins.csvreader import CSVReader
# from locust import HttpUser, task

# ssn_reader = CSVReader("ssn.csv")


# class MyUser(HttpUser):
#     @task
#     def index(self):
#         customer = next(ssn_reader)
#         self.client.get(f"/?ssn={customer[0]}")

#     host = "http://example.com"