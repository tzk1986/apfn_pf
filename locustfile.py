import time
from locust import HttpUser, constant, constant_pacing, constant_throughput, task, between
import queue
from tools.loader import read_csv_file


class QuickstartUser(HttpUser) :
    
    host = 'http://10.50.11.120:9001'
    
    # wait_time = between(1, 5)
    wait_time = constant_throughput(50)
    # wait_time = constant_pacing(1)
    # wait_time = constant(1)
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.q = queue.Queue()  # 初始化一个队列
    
    # def on_start(self):
    #     csv_list = read_csv_file("data.csv")
    #     for i in csv_list:
    #         self.q.put(i)  # 将数据添加到队列中

    @task
    def hello_world(self):
        # self.client.get("/vip/vip/list")
        self.client.get("/vip/face/list")

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})