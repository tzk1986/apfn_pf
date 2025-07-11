# 1. 使用列表（占用更多内存）
def get_squares_list(n):
    return [x * x for x in range(n)]


# 2. 使用生成器（内存效率更高）
def get_squares_generator(n):
    for x in range(n):
        yield x * x


# 内存使用对比
import sys

numbers_list = get_squares_list(1000000)
numbers_gen = get_squares_generator(1000000)
print(numbers_list[0])
print(next(numbers_gen))

print(f"列表占用内存: {sys.getsizeof(numbers_list)} 字节")
print(f"生成器占用内存: {sys.getsizeof(numbers_gen)} 字节")


# Distributing test data 支持将测试数据从主服务器分发到工作程序，同时维护测试数据顺序
# this example is a little more complex than it needs to be, but I wanted to highlight
# that it is entirely possible to have multiple distributors at the same time

from typing import Dict, List
from locust_plugins.csvreader import CSVDictReader, CSVReader
from locust_plugins.distributor import Distributor
from locust import HttpUser, task, run_single_user, events
from locust.runners import WorkerRunner

distributors = {}


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    ssn_iterator = None
    product_iterator = None
    if not isinstance(environment.runner, WorkerRunner):
        product_iterator = CSVReader("products.csv")
        ssn_iterator = CSVDictReader("ssn.tsv", delimiter="\t")
        # other readers work equally well
        # ssn_reader = MongoLRUReader({"foo": "bar"}, "last_login")
    distributors["products"] = Distributor(environment, product_iterator, "products")
    distributors["customers"] = Distributor(environment, ssn_iterator, "customers")


class MyUser(HttpUser):
    host = "http://www.example.com"

    @task
    def my_task(self) -> None:
        product: List[str] = next(distributors["products"])
        customer: Dict = next(distributors["customers"])
        self.client.get(f"/?product={product[0]}&customer={customer['ssn']}")


if __name__ == "__main__":
    run_single_user(MyUser)


# Transaction manager 事务管理器，记录并按顺序进行task，忽略了任务权重
from locust import HttpUser, task, SequentialTaskSet
from locust_plugins.transaction_manager import TransactionManager


class ExampleSequentialTaskSet(SequentialTaskSet):
    def on_start(self):
        self.tm = TransactionManager()

    @task
    def home(self):
        self.tm.start_transaction("startup")
        self.client.get("/", name="01 /")

    @task
    def get_config_json(self):
        self.client.get("/config.json", name="02 /config.json")
        self.tm.end_transaction("startup")


class TranactionExample(HttpUser):
    host = "https://www.demoblaze.com"

    tasks = [ExampleSequentialTaskSet]
