import queue
import requests
import json
from tools.csvreader_cn import CSVDictReader,CSVReader

url = "http://10.50.11.75:11000/capi/unified/pay"

querystring = {"scene":"MULTI"}

payload = {
    "sellerPid": "256",
    "buyerPid": "4096",
    "orderAmount": 0.01,
    "requestId": "MULTI_094"
}
headers = {
    "tenantId": "8a8b88e2718b20b1b6e19b2b0414a1ea",
    "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
    "Accept": "*/*",
    "Host": "10.50.11.75:11000",
    "Connection": "keep-alive",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

print(response.json()['errCode'])


def incrementer(start=0):
    """
    自增迭代器生成函数
    :param start: 起始数值
    :yield: 自增的数值
    """
    current = start
    while True:
        yield current
        current += 1  # 自增
        
# 生成自增的迭代器



list1 = ["24121000001","24121000003","24121000004","24121300001","24121100001"]
q = queue.Queue()
for data in list1:
    print(data)
    q.put(data)

if __name__ == '__main__':
    incrementer_gen = incrementer(99)
    for _ in range(10):
        print(f"MULTI_{next(incrementer_gen):03d}")
        
        
buyerPid = CSVReader("./data/buyerPid.csv")

data = next(buyerPid)[0]
print(data)
