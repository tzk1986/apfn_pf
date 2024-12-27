# 导入所需的库
from locust import HttpUser, LoadTestShape, task, between
import requests  # 导入locust相关类和装饰器
from tools.data_factory import get_register_data  # 导入生成测试数据的工具函数
import random  # 导入随机数模块
from tools.loader import read_csv_file
import queue
from tools.csvreader_cn import CSVDictReader
from locust_plugins import constant_total_ips


# 使用生成器读取CSV文件，不用再用queue队列，内存效率更高
data_list = CSVDictReader("./data/20241126.csv")


    
    
# def get_login_token():
#     """获取登录token的函数"""
#     login_url = "http://10.50.11.120:9001/api/login"  # 替换为实际登录地址
#     login_data = {
#         "username": "your_username",
#         "password": "your_password"
#     }
    
#     try:
#         response = requests.post(login_url, json=login_data)
#         if response.status_code == 200:
#             # 根据实际响应格式获取token
#             token = response.json().get('data', {}).get('token')
#             return token
#         else:
#             raise Exception(f"登录失败: {response.text}")
#     except Exception as e:
#         # 打印获取token失败的错误信息,方便调试和排查问题
#         print(f"获取token失败: {str(e)}")
#         return None

# # 在启动时获取token
# TOKEN = get_login_token()


class PayUser(HttpUser):
    """支付用户类,用于模拟用户支付行为"""
    host = "http://10.50.11.120:9001"
    
    # 设置固定的总请求速率为每秒2次请求，如果task中请求只有一个，那么RPS=IPS，
    # 如果task中请求有多个，那么RPS=IPS*请求个数
    wait_time = constant_total_ips(100)
    
    # def on_start(self):
    #     """
    #     在测试开始前执行,用于初始化数据
    #     该方法会在每个用户实例开始测试前被调用一次
    #     """
    #     # 获取一条用户数据用于支付,包含姓名、电话、地址等信息
    #     self.user_data = get_register_data(1)[0]
        
    #     # 设置支付相关参数
    #     self.pay_types = ['alipay', 'wechat', 'unionpay']  # 支持的支付方式列表
    #     self.amounts = [99.9, 199.9, 299.9, 399.9, 499.9]  # 可选的支付金额列表
    
    @task # 设置任务权重为1
    def pay_order(self):
        """
        模拟支付请求
        发送POST请求到支付接口,携带用户信息和支付信息
        """
        # 构建支付请求的数据负载
        # payload = {
        #             "remark": None,
        #             "orderAmount": "1",
        #             "accountType": 1,
        #             "accountBalanceId": "4619d6b21e244c8db26d0e6d0439966c",
        #             "merchantId": "2021040701",
        #             "userId": "USERg100956702",
        #             "welfareId": None,
        #             "requireAmount": "1",
        #             "actualAmount": 1,
        #             "discountAmount": 0,
        #             "welfareAmount": 0,
        #             "channelTypeList": None,
        #             "merchantName": "上海艾佩菲宁",
        #             "phoneNumber": "15900506254",
        #             "nickName": "微信用户"
        #          }
        payload = next(data_list)
        # print(payload)
        headers = {"Token": "1E29063B7B1B024CF6831FB9EC736A3E"}
        # headers = {"Token": TOKEN}
        
        # 发送POST请求到支付接口
        with self.client.post(
            "/api/ts/accountBalance/chargeDirect",           # 支付接口地址
            json=payload,         # JSON格式的请求数据
            headers=headers,
            catch_response=True,   # 捕获响应以便自定义处理
            name="充值接口"
        ) as response:
            # 判断请求是否成功
            # print(response.json())
            if response.json()['message'] == "调用成功":
                response.success()  # 标记为成功
            else:
                response.failure(f"支付失败: {response.text}")  # 标记为失败并记录错误信息

                
# 自定义用户增量曲线
# class StagesShapeWithCustomUsers(LoadTestShape):

#     stages = [
#         {"duration": 20, "users": 1, "spawn_rate": 1, "user_classes": [PayUser]},
#         {"duration": 40, "users": 2, "spawn_rate": 1, "user_classes": [PayUser, ]},
#         {"duration": 60, "users": 3, "spawn_rate": 1, "user_classes": [PayUser]},
#         {"duration": 100, "users": 4, "spawn_rate": 1, "user_classes": [PayUser,]},
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

#         return None

if __name__ == '__main__':
    # 运行命令: locust -f Pay.py
    # 启动locust后,可以通过Web界面设置并发用户数和运行时间等参数
    pass
