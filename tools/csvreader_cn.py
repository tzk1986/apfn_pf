# import csv
# from typing import Iterator, Dict
# # 在from locust_plugins.csvreader import CSVDictReader基础上修改，增加utf-8编码读取文件

# class CSVReader(Iterator):
#     "Read test data from csv file using an iterator"

#     def __init__(self, file, **kwargs):
#         try:
#             file = open(file)
#         except TypeError:
#             pass  # "file" was already a pre-opened file-like object
#         self.file = file
#         self.reader = csv.reader(file, **kwargs)

#     def __next__(self):
#         try:
#             return next(self.reader)
#         except StopIteration:
#             # reuse file on EOF
#             self.file.seek(0, 0)
#             return next(self.reader)


# class CSVDictReader(Iterator[Dict]):
#     "Read test data from csv file using an iterator, returns rows as dicts"

#     def __init__(self, file, **kwargs):
#         try:
#             file = open(file,encoding='utf-8')
#         except TypeError:
#             pass  # "file" was already a pre-opened file-like object
#         self.file = file
#         self.reader = csv.DictReader(file, **kwargs)

#     def __next__(self):
#         try:
#             return next(self.reader)
#         except StopIteration:
#             # reuse file on EOF 
#             self.file.seek(0, 0)
#             next(self.reader)  # skip header line
#             return next(self.reader)
#             # raise # 注释上面两行代码，不循环读取文件，直接结束



'''
优化
1.文件打开方式:

在 CSVDictReader 中，打开文件时使用 with 语句可以确保文件在使用后自动关闭，避免文件句柄泄漏。
2.异常处理:

可以更清晰地处理文件打开的异常，比如捕获具体的异常类型。
3.去掉重复代码:

CSVReader 和 CSVDictReader 中的文件打开和异常处理逻辑有重复，可以考虑将其提取到一个基类中。
4.改进重置逻辑:

在 __next__ 方法中，可以考虑使用一个标志来指示是否需要跳过表头，而不是总是跳过。
'''
import csv
from typing import Iterator, Dict

class BaseCSVReader(Iterator):
    "Base class for CSV readers"

    def __init__(self, file, **kwargs):
        if isinstance(file, str):
            self.file = open(file, encoding='utf-8')
        else:
            self.file = file
        self.reader = None

    def reset(self):
        self.file.seek(0, 0)

    def close(self):
        self.file.close()

class CSVReader(BaseCSVReader):
    "Read test data from csv file using an iterator"

    def __init__(self, file, **kwargs):
        super().__init__(file, **kwargs)
        self.reader = csv.reader(self.file, **kwargs)

    def __next__(self):
        try:
            return next(self.reader)
        except StopIteration:
            self.reset()
            return next(self.reader)

class CSVDictReader(BaseCSVReader):
    "Read test data from csv file using an iterator, returns rows as dicts"

    def __init__(self, file, **kwargs):
        super().__init__(file, **kwargs)
        self.reader = csv.DictReader(self.file, **kwargs)

    def __next__(self):
        try:
            return next(self.reader)
        except StopIteration:
            self.reset()
            next(self.reader)  # skip header line
            return next(self.reader)