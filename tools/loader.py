import csv
from typing import Text


def read_csv_file(csv_file: Text) -> list:
    """
    读取CSV文件并将其转换为列表，保持原始数据类型

    :param csv_file: CSV文件的路径
    :return: 一个列表的列表,其中每个内部列表代表CSV文件中的一行
    """

    def convert_value(value):
        """
        转换值为适当的数据类型，确保与API请求参数格式兼容
        """
        # 处理空值、None和null
        if value is None or value.strip().lower() in ["none", "null", ""]:
            return None

        try:
            # 处理数字类型
            if value.isdigit():
                # 纯数字字符串，根据长度判断是否需要用字符串类型
                if len(value) > 10:  # 例如处理长数字ID
                    return str(value)
                return int(value)

            # 尝试转换为浮点数
            float_val = float(value)
            # 某些特殊场景可能需要保持字符串格式
            if "." in value:  # 如金额等需要精确表示的数值
                return str(float_val)
            return float_val
        except ValueError:
            # 非数字类型保持原字符串
            return value

    csv_content_list = []
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 转换每个值为适当的数据类型
            converted_row = {k: convert_value(v) for k, v in row.items()}
            csv_content_list.append(converted_row)
    return csv_content_list


if __name__ == "__main__":
    data_list = read_csv_file("./data/20241126.csv")
    print(data_list[0])
