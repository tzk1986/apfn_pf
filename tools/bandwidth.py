

def calculate_bandwidth(RPS:int)->float:
    # 假设每个请求
    request_size = 1024  # 请求大小(bytes)
    response_size = 2048  # 响应大小(bytes)
    total_size = (request_size + response_size)  # 单个请求总流量
    # total_size = 4392
    
    # 当前RPS
    current_rps = RPS # 每秒请求数
    
    # 理论带宽使用
    bandwidth_per_second = total_size * current_rps
    bandwidth_mbps = (bandwidth_per_second * 8) / (1024 * 1024)  # 转换为Mbps
    
    return bandwidth_mbps

if __name__ == "__main__":
    print(calculate_bandwidth(103))
