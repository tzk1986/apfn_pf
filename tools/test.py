# 1. 使用列表（占用更多内存）
def get_squares_list(n):
    return [x*x for x in range(n)]

# 2. 使用生成器（内存效率更高）
def get_squares_generator(n):
    for x in range(n):
        yield x*x

# 内存使用对比
import sys
numbers_list = get_squares_list(1000000)
numbers_gen = get_squares_generator(1000000)
print(numbers_list[0])
print(next(numbers_gen))

print(f"列表占用内存: {sys.getsizeof(numbers_list)} 字节")
print(f"生成器占用内存: {sys.getsizeof(numbers_gen)} 字节")