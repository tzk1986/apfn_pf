# from locust import HttpUser, task

# class HelloWorldUser(HttpUser):
#     @task
#     def hello_world(self):
#         self.client.get("/vip/vip/list")
#         self.client.get("/vip/face/list")
        
        
import time
from locust import HttpUser, constant, constant_pacing, constant_throughput, task, between

class QuickstartUser(HttpUser):
    # wait_time = between(1, 5)
    wait_time = constant_throughput(50)
    # wait_time = constant_pacing(1)
    # wait_time = constant(1)

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