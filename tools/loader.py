import csv
from typing import Text


def read_csv_file(csv_file: Text):
    """
    读取CSV文件并将其转换为列表

    :param csv_file: CSV文件的路径
    :return: 一个列表的列表,其中每个内部列表代表CSV文件中的一行
    """
    csv_content_list = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_content_list.append(row)
    return csv_content_list
