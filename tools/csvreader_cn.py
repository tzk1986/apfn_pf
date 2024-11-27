import csv
from typing import Iterator, Dict
# 在from locust_plugins.csvreader import CSVDictReader基础上修改，增加utf-8编码读取文件

class CSVReader(Iterator):
    "Read test data from csv file using an iterator"

    def __init__(self, file, **kwargs):
        try:
            file = open(file)
        except TypeError:
            pass  # "file" was already a pre-opened file-like object
        self.file = file
        self.reader = csv.reader(file, **kwargs)

    def __next__(self):
        try:
            return next(self.reader)
        except StopIteration:
            # reuse file on EOF
            self.file.seek(0, 0)
            return next(self.reader)


class CSVDictReader(Iterator[Dict]):
    "Read test data from csv file using an iterator, returns rows as dicts"

    def __init__(self, file, **kwargs):
        try:
            file = open(file,encoding='utf-8')
        except TypeError:
            pass  # "file" was already a pre-opened file-like object
        self.file = file
        self.reader = csv.DictReader(file, **kwargs)

    def __next__(self):
        try:
            return next(self.reader)
        except StopIteration:
            # reuse file on EOF 
            self.file.seek(0, 0)
            next(self.reader)  # skip header line
            return next(self.reader)
            # raise # 注释上面两行代码，不循环读取文件，直接结束

