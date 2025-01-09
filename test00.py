import logging

# 配置日志记录器
logging.basicConfig(
    filename='./data/test_log.log',  # 日志文件路径
    level=logging.INFO,            # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
)

# 测试日志记录
logging.info("这是一条测试日志记录")
logging.warning("这是一条警告日志记录")
logging.error("这是一条错误日志记录")
