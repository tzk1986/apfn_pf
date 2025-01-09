import logging
from locust import HttpUser, LoadTestShape, task, between
from datetime import datetime
import requests  # 导入locust相关类和装饰器
import random  # 导入随机数模块
from tools.csvreader_cn import CSVDictReader,CSVReader
from locust_plugins import constant_total_ips
import json

# 配置日志
logging.basicConfig(
    filename='./data/pay_order.log',  # 日志文件路径
    level=logging.INFO,            # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
)

# 日志记录开关
LOGGING_ENABLED = True
# LOGGING_ENABLED = False

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
incrementer_gen = incrementer(442861)

# 记录上次使用到哪个编号442860

# 如果需要增加用户，只需要在csv文件中增加就行
data = CSVReader("./data/buyerPid_ol.csv")

data2 = CSVReader("./data/sellerPid_ol.csv")

# 全局变量记录总带宽使用量
total_bandwidth = 0

class PayUser(HttpUser):
    """支付用户类,用于模拟用户支付行为"""
    host = "https://dsp.lgdefu.com/ups"
    wait_time = constant_total_ips(400)  # 设置固定的总请求速率为每秒200次请求

    @task
    def pay_order(self):
        global total_bandwidth
        """
        模拟支付请求
        发送POST请求到支付接口,携带用户信息和支付信息
        """
        # 构建支付请求的数据负载
        buyerPid = next(data)[0]
        sellerPid = next(data2)[0]
        querystring = {"scene":"MULTI"}
        current_requestId = f"MULTI_{next(incrementer_gen):03d}"
        payload = {
            "sellerPid": sellerPid,
            "buyerPid": buyerPid,
            "orderAmount": 0.01,
            "requestId": current_requestId,
        }
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        # print(f"{formatted_time}：用户{buyerPid}编号{current_requestId}")
        if LOGGING_ENABLED:
            logging.info(f"{formatted_time}：用户{buyerPid}编号{current_requestId}")
        headers = {
            "tenantId": "6415488620d6846f3836db032815f6a5",
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }

        # 发送POST请求到支付接口
        with self.client.post(
            "/capi/unified/pay",           # 支付接口地址
            json=payload,         # JSON格式的请求数据
            headers=headers,
            params=querystring,
            catch_response=True,   # 捕获响应以便自定义处理
            name="支付接口"
        ) as response:
            # 计算请求和响应的大小
            request_size = len(json.dumps(payload)) + sum(len(k) + len(v) for k, v in headers.items())
            response_size = len(response.content)
            total_size = request_size + response_size

            # 更新总带宽使用量
            total_bandwidth += total_size

            # 判断请求是否成功
            if response.json()['errCode'] == 0:
                response.success()  # 标记为成功
                # logging.info(f"支付成功: buyerPid:{buyerPid} requestId:{current_requestId}")
            else:
                response.failure(f"支付失败: buyerPid:{buyerPid} {response.text}")  # 标记为失败并记录错误信息
                if LOGGING_ENABLED:
                    logging.error(f"支付失败: buyerPid:{buyerPid} {response.text}")

            # 记录带宽使用情况
            if LOGGING_ENABLED:
                bandwidth_mb_s = total_bandwidth / (1024 * 1024)  # Convert to MB/s
                logging.info(f"请求大小: {request_size} bytes, 响应大小: {response_size} bytes, 总大小: {total_size} bytes, 总带宽使用量: {bandwidth_mb_s:.2f} MB/s")
