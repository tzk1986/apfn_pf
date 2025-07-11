import time
from locust import (
    FastHttpUser,
    LoadTestShape,
    constant,
    constant_pacing,
    constant_throughput,
    task,
    between,
)
import queue
from tools.loader import read_csv_file
from tools.data_factory import get_register_data


class QuickstartUser(FastHttpUser):
    # 被测系统的host
    host = "http://10.50.11.120:9001"
    # 报告生成路径
    html = "./reports/index.html"

    # 设置并发用户等待时间为0-1秒
    # wait_time = between(0, 1)

    # 混合场景用到
    # wait_time = constant_throughput(100) # 提高每秒请求数上限
    # wait_time = constant_pacing(0.5) # 缩短固定等待时间
    # wait_time = constant(0.5)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.q = queue.Queue()  # 初始化一个队列

    # def on_start(self):
    #     csv_list = read_csv_file("data.csv")
    #     for i in csv_list:
    #         self.q.put(i)  # 将数据添加到队列中

    @task(3)  # 增加任务权重
    def hello_world(self):
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
            if res.status_code == 200:
                res.success()
            else:
                res.failure("请求失败")

    # @task(2)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(0.5) # 减少等待时间


# 自定义用户增量曲线
class StagesShapeWithCustomUsers(LoadTestShape):

    stages = [
        {"duration": 10, "users": 1, "spawn_rate": 1, "user_classes": [QuickstartUser]},
        {"duration": 20, "users": 2, "spawn_rate": 1, "user_classes": [QuickstartUser]},
        {"duration": 30, "users": 3, "spawn_rate": 1, "user_classes": [QuickstartUser]},
        {"duration": 40, "users": 4, "spawn_rate": 1, "user_classes": [QuickstartUser]},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                try:
                    tick_data = (
                        stage["users"],
                        stage["spawn_rate"],
                        stage["user_classes"],
                    )
                except:
                    tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None
