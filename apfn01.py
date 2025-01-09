# 导入所需的库
import csv
import json
import logging
from locust import HttpUser, LoadTestShape, constant, task, between
from datetime import datetime
import requests  # 导入locust相关类和装饰器
from tools.data_factory import get_register_data  # 导入生成测试数据的工具函数
import random  # 导入随机数模块
from tools.loader import read_csv_file
import queue
from tools.csvreader_cn import CSVDictReader,CSVReader
from locust_plugins import constant_total_ips
import time


# 配置日志
logging.basicConfig(
    filename='./data/pay_order.log',  # 日志文件路径
    level=logging.INFO,            # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
)

# 日志记录开关
LOGGING_ENABLED = True

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
incrementer_gen = incrementer(172300)

# 记录上次使用到哪个编号 138764

incrementer_gen2 = incrementer(172300)

# 如果需要增加用户，只需要在csv文件中增加就行
data = CSVReader("./data/buyerPid.csv")

# list1 = ["24121000001","24121000003","24121000004","24121300001","24121100001"]
# q = queue.Queue()
# for data in list1:
#     q.put(data)


class PayUser(HttpUser):
    """支付用户类,用于模拟用户支付行为"""
    host = "http://10.50.11.75:11000"
    # host = "https://dsp.lgdefu.com/ups"
    # 设置请求间隔为1-3秒,模拟真实用户操作间隔
    # 设置固定的总请求速率为每秒2次请求，如果task中请求只有一个，那么RPS=IPS，
    # 如果task中请求有多个，那么RPS=IPS*请求个数
    # wait_time = constant_total_ips(30)

    # 类变量，用于存储 current_requestId 和支付状态
    current_requestId = None
    payment_successful = False
    
    @task(10)
    def pay_order(self):
        """
        模拟支付请求
        发送POST请求到支付接口,携带用户信息和支付信息
        """
        # 构建支付请求的数据负载
        buyerPid = next(data)[0]
        querystring = {"scene":"MULTI"}
        PayUser.current_requestId = f"MULTI_{next(incrementer_gen):03d}"
        payload = {
            "sellerPid": "256",
            "buyerPid": buyerPid,
            # 4096 24121000004
            "orderAmount": 0.01,
            "requestId": PayUser.current_requestId,
        }
        # payload = next(data_list)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        # print(f"{formatted_time}：用户{buyerPid}编号{PayUser.current_requestId}")
        logging.info(f"{formatted_time}：用户{buyerPid}编号{PayUser.current_requestId}")
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
                # 将 current_requestId 存储到 xxx.csv 文件中
                with open('./data/xxx.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([PayUser.current_requestId])
            else:
                response.failure(f"支付失败: buyerPid:{buyerPid}{response.text}")  # 标记为失败并记录错误信息                
            end_time = time.time()
            request_size = len(json.dumps(payload)) + sum(len(k) + len(v) for k, v in headers.items())
            response_size = len(response.content)
            total_size = request_size + response_size
            duration = end_time - start_time
            bandwidth = total_size / duration
            # print(f"Request size: {request_size} bytes, Response size: {response_size} bytes, Total size: {total_size} bytes, Duration: {duration} seconds, Bandwidth: {bandwidth} bytes/second")
            logging.info(f"Request size: {request_size} bytes, Response size: {response_size} bytes, Total size: {total_size} bytes, Duration: {duration} seconds, Bandwidth: {bandwidth} bytes/second")
        
        
    @task(1)   
    def refund(self):
        """
        模拟退款请求
        """
        # 从 xxx.csv 文件中读取 current_requestId
        with open('./data/xxx.csv', mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                PayUser.current_requestId = rows[0][0]  # 读取第一个请求ID
                # 删除已使用的数据
                with open('./data/xxx.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows[1:])
            else:
                logging.error("没有找到支付请求ID，无法进行退款")
                return

        querystring = {"scene":"MULTI"}
        refund_requestId = f"M_REFUND_ID_{next(incrementer_gen2):03d}"
        payload = {
            "payRequestId": PayUser.current_requestId,
            "requestId": refund_requestId,
            "orderAmount": 0.01
        }
        headers = {
            "tenantId": "8a8b88e2718b20b1b6e19b2b0414a1ea",
            "Content-Type": "application/json"
        }

        # 发送POST请求到退款接口
        with self.client.post("/capi/unified/refund", json=payload, headers=headers, params=querystring, catch_response=True, name="退款接口") as response:
            if response.json()['errCode'] == 0:
                response.success()  # 标记为成功
                if LOGGING_ENABLED:
                    logging.info(f"退款成功: payRequestId:{payload['payRequestId']} requestId:{payload['requestId']}")
            else:
                response.failure(f"退款失败:{response.text}")  # 标记为失败并记录错误信息
                if LOGGING_ENABLED:
                    logging.error(f"退款失败: payRequestId:{payload['payRequestId']} {response.text}")
            logging.info(response.text)