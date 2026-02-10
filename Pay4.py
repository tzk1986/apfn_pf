# 导入所需的库
from locust import HttpUser, LoadTestShape, task, between
import requests  # 导入locust相关类和装饰器
from tools.data_factory import get_register_data  # 导入生成测试数据的工具函数
import random  # 导入随机数模块
from tools.loader import read_csv_file
import queue
from tools.csvreader_cn import CSVDictReader
from locust_plugins import constant_total_ips
import itertools
import csv


"""
模拟大批量点餐数据，使用csv文件准备不同参数，进行数据的差异化，
不同的卡号，不同档口不同菜品数据生成

"""

# 使用生成器读取CSV文件，不用再用queue队列，内存效率更高
data_list = CSVDictReader("./data/20241126.csv")


# 读取卡号数据，创建循环迭代器用于数据驱动
def load_card_numbers(filepath):
    """从CSV文件加载卡号列表"""
    card_numbers = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                card_number = line.strip().strip('"')  # 去除换行符和引号
                if card_number:
                    card_numbers.append(card_number)
    except Exception as e:
        print(f"加载卡号文件失败: {e}")
    return card_numbers

# 读取档口菜品数据，创建循环迭代器用于数据驱动
def load_store_food_data(filepath):
    """从CSV文件加载档口菜品数据"""
    store_food_list = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row:
                    store_food_list.append(row)
    except Exception as e:
        print(f"加载档口菜品文件失败: {e}")
    return store_food_list

# 加载卡号列表并创建无限循环迭代器
card_numbers = load_card_numbers("./data/cardnum.csv")
card_number_iterator = itertools.cycle(card_numbers) if card_numbers else itertools.cycle(["10308129"])

# 加载档口菜品数据并创建无限循环迭代器
store_food_data = load_store_food_data("./data/store_food_data.csv")
store_food_iterator = itertools.cycle(store_food_data) if store_food_data else itertools.cycle([{
    'storeId': '9ddc9145f0c44fcc8bb69b2b3fb30a6a',
    'storeName': '档口A',
    'foodId': '412bb78f12774eb8be931ac97df4ec7b',
    'foodName': '辣椒炒肉',
    'price': '0.50',
    'vipPrice': '0.40'
}])




class PayUser(HttpUser):
    """支付用户类,用于模拟用户点餐支付行为"""
    host = "http://10.50.11.22:8090"  # 使用22环境 中芯环境，设备端口8090
    
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
        模拟点餐支付请求
        发送POST请求到支付接口,携带用户信息和支付信息
        """
        # 从迭代器获取下一个卡号
        current_card_number = next(card_number_iterator)
        
        # 从迭代器获取下一个档口菜品数据
        current_store_food = next(store_food_iterator)
        
        # 获取档口和菜品信息
        store_id = current_store_food['storeId']
        food_id = current_store_food['foodId']
        food_name = current_store_food['foodName']
        price = float(current_store_food['price'])
        vip_price = float(current_store_food['vipPrice'])
        
        # 构建点餐支付请求的数据负载
        payload = {
                    "autoPayStatus": 0,
                    "cashAmount": 0,
                    "discountAmount": 0.00,
                    "machineCode": "5AD2522017572256",
                    "merchantId": "2025081807", # 商户ID
                    "orderAmount": vip_price,
                    "orderCode": "",
                    "orderOriginal": 4, # 订单来源 4-点餐
                    "payAmount": 0,
                    "payType": 2, # 支付方式 2-刷卡
                    "paymentAmount": vip_price,
                    "qrCode": current_card_number, # 卡号 从CSV循环读取卡号数据
                    "storeId": store_id, # 档口ID 从CSV循环读取档口数据
                    "uploadGoodsOneList": [{
                                            "consumptionAmount": vip_price,
                                            "count": 1,
                                            "endDateStr": "2025-12-04 10:50:44",
                                            "foodId": food_id, # 菜品ID 从CSV循环读取菜品数据
                                            "foodName": food_name, # 菜品名称 从CSV循环读取菜品数据
                                            "heat": 0,
                                            "isCombom": False,
                                            "machineId": "5AD2522017572256",
                                            "merchantId": "2025081807",# 商户ID
                                            "price": price,
                                            "startDateStr": "2025-12-04 09:50:44",
                                            "storeId": store_id, # 档口ID 从CSV循环读取档口数据
                                            "userType": 0,
                                            "vipPrice": vip_price,
                                            "weight": 0
                                            }]
                    
                }
        # payload = next(data_list)
        # print(payload)
        headers = {"Token": "05B8E6D3F72BBB5CB5274A6A7B0DDB3F"}
        # headers = {"Token": TOKEN}
        
        # 发送POST请求到点餐支付接口
        with self.client.post(
            "/machine/createOrderAndGoodsPay",    # 点餐地址
            json=payload,         # JSON格式的请求数据
            headers=headers,
            catch_response=True,   # 捕获响应以便自定义处理
            name="点餐接口"
        ) as response:
            # 判断请求是否成功
            # print(response.json())
            if response.json()['message'] == "调用成功":
                response.success()  # 标记为成功
            else:
                response.failure(f"点餐失败: {response.text}")  # 标记为失败并记录错误信息

                
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
    # print(card_numbers)
    pass
