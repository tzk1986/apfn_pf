import json
import logging  # Add logging module
from locust import HttpUser, LoadTestShape, task, between, TaskSet
from tools.csvreader_cn import CSVDictReader, CSVReader
from locust_plugins import constant_total_ips
from datetime import datetime
import time

# Logging configuration
log_file_path = './data/test_log.log'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.FileHandler(log_file_path)])


log_print_content = True  # Switch to enable/disable logging of printed content
log_bandwidth_usage = True  # Switch to enable/disable logging of bandwidth usage


def incrementer(start=0):
    """
    自增迭代器生成函数
    :param start: 起始数值
    :yield: 自增的数值
    """
    current = start
    while True:
        yield current
        current += 1  # 自增r
        
# 生成自增的迭代器
incrementer_gen = incrementer(34325)

# 记录上次使用到哪个编号34324

# 如果需要增加用户，只需要在csv文件中增加就行
data = CSVReader("./data/buyerPid.csv")

class StepLoadShape(LoadTestShape):
    """
    A step load shape that adds users at a fixed interval.
    起始用户数量为10，每五分钟增加10个用户，持续15分钟
    """

    step_time = 300  # Time between steps (in seconds)
    step_load = 1   # Users to add at each step
    spawn_rate = 1 # Users to spawn per second
    time_limit = 60  # Total test duration (in seconds)

    def tick(self):
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = run_time // self.step_time
        return (10 + current_step * self.step_load, self.spawn_rate)

# Add this shape to your Locust test
class UserBehavior(TaskSet):
    @task
    def pay_order(self):
        """
        模拟支付请求
        发送POST请求到支付接口,携带用户信息和支付信息
        """
        # 构建支付请求的数据负载
        buyerPid = next(data)[0]
        querystring = {"scene":"MULTI"}
        current_requestId = f"MULTI_{next(incrementer_gen):03d}"
        payload = {
            "sellerPid": "256",
            "buyerPid": buyerPid,
            # 4096 24121000004
            "orderAmount": 0.01,
            "requestId": current_requestId,
        }
        # payload = next(data_list)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{formatted_time}：用户{buyerPid}编号{current_requestId}"
        print(log_message)
        if log_print_content:
            logging.info(log_message)
        headers = {
            "tenantId": "8a8b88e2718b20b1b6e19b2b0414a1ea",
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Accept": "*/*",
            "Host": "10.50.11.75:11000",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }
        # headers = {"Token": TOKEN}

        # 发送POST请求到支付接口
        start_time = time.time()
        with self.client.post(
            "/capi/unified/pay",           # 支付接口地址
            json=payload,         # JSON格式的请求数据
            headers=headers,
            params=querystring,
            catch_response=True,   # 捕获响应以便自定义处理
            name="支付接口"
        ) as response:
            # 判断请求是否成功
            # print(response.json())
            if response.json()['errCode'] == 0:
                response.success()  # 标记为成功
            else:
                response.failure(f"支付失败: buyerPid:{buyerPid}{response.text}")  # 标记为失败并记录错误信息
            end_time = time.time()
            request_size = len(json.dumps(payload)) + sum(len(k) + len(v) for k, v in headers.items())
            response_size = len(response.content)
            total_size = request_size + response_size
            duration = end_time - start_time
            bandwidth = total_size / duration
            bandwidth_mb_s = bandwidth / (1024 * 1024)  # Convert to MB/s
            bandwidth_message = f"Request size: {request_size} bytes, Response size: {response_size} bytes, Total size: {total_size} bytes, Duration: {duration} seconds, Bandwidth: {bandwidth_mb_s:.2f} MB/s"
            print(bandwidth_message)
            if log_bandwidth_usage:
                logging.info(bandwidth_message)

class WebsiteUser(HttpUser):
    host = "http://10.50.11.75:11000"
    tasks = [UserBehavior]
    wait_time = between(1, 5)
    load_shape = StepLoadShape