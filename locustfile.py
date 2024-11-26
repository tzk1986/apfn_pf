import time
from locust import HttpUser, LoadTestShape, constant, constant_pacing, constant_throughput, task, between
import queue
from tools.loader import read_csv_file
from tools.data_factory import get_register_data


class QuickstartUser(HttpUser) :
    # 被测系统的host
    host = 'http://10.50.11.120:9001'
    # 报告生成路径
    html = './reports/index.html'

    # wait_time = between(1, 5)
    # 混合场景用到
    # wait_time = constant_throughput(50) # 每秒每个用户一个请求RPS上限值
    # wait_time = constant_pacing(1)
    # wait_time = constant(1)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.q = queue.Queue()  # 初始化一个队列

    # def on_start(self):
    #     csv_list = read_csv_file("data.csv")
    #     for i in csv_list:
    #         self.q.put(i)  # 将数据添加到队列中

    # @task
    # def register_user(self):
    #     # 使用mimesis的工具模块生成注册数据
    #     data = get_register_data(1)

    @task
    def hello_world(self):
        # self.client.get("/vip/vip/list")
        with self.client.post(
            "/api/query/userInfos",
            json={
                "userBackStatus": "0",
                "phoneNumber": "",
                "nickName": "",
                "memberCard": "",
                "merchantId": "2021040701",
                "pageNum": 1,
                "delFlag": 0,
                "pageSize": 10,
                "sysId": "iom",
            },
            headers={"Token": "8E3230CD241D57A0EF238B47517578DB"},
            name="会员-人脸列表",
            catch_response=True,
        ) as res:
            # print(res.json())
            if res.status_code == 200:
                res.success()
            else:
                res.failure("请求失败")

        # try: # 手动断言
        #     assert self.q.qsize() > 0
        # except AssertionError:
        #     print("No more data to process")
        #     exit()

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)


# 自定义用户增量曲线
# class StagesShapeWithCustomUsers(LoadTestShape):

#     stages = [
#         {"duration": 10, "users": 10, "spawn_rate": 10, "user_classes": [QuickstartUser]},
#         {"duration": 30, "users": 50, "spawn_rate": 10, "user_classes": [QuickstartUser, ]},
#         {"duration": 60, "users": 100, "spawn_rate": 10, "user_classes": [QuickstartUser]},
#         {"duration": 120, "users": 100, "spawn_rate": 10, "user_classes": [QuickstartUser,]},
#     ]

#     def tick(self):
#         run_time = self.get_run_time()

#         for stage in self.stages:
#             if run_time < stage["duration"]:
#                 try:
#                     tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
#                 except:
#                     tick_data = (stage["users"], stage["spawn_rate"])
#                 return tick_data
#         # for stage in self.stages:
#         #     if run_time < stage["duration"]:
#         #         tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
#         #         return tick_data
#         return None
