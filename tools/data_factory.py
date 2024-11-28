from mimesis import Person
from mimesis.locales import Locale
from mimesis.schema import Schema
from mimesis import Address
import random


def get_register_data(x:int=1)->list:
    """
    使用mimesis生成注册数据
    
    Args:
        x (int): 需要生成的数据条数,默认为1条
        
    Returns:
        list: 包含生成数据的列表,每条数据为一个字典,包含以下字段:
            - name: 姓名
            - gender: 性别 
            - work: 职业
            - address: 详细地址
            - province: 省份
            - city: 城市
            - phone: 电话号码
            - marriage: 婚姻状况(已婚/未婚)
    """
    # 创建Person实例,使用中文locale
    p = Person(Locale.ZH)
    # 创建Address实例,使用中文locale 
    a = Address(Locale.ZH)
    
    # 定义数据生成schema
    schema = Schema(
        schema=lambda: {
            'name': p.full_name(),      # 生成全名
            'gender': p.gender(),       # 生成性别
            'work': p.occupation(),     # 生成职业
            'address': a.address(),     # 生成详细地址
            'province': a.province(),   # 生成省份
            'city': a.city(),          # 生成城市
            'phone': p.telephone(),     # 生成电话号码
            'marriage': random.choice(['已婚', '未婚'])  # 随机生成婚姻状况
        },
        iterations=x)  # 指定生成数据条数
    
    # 返回生成的数据列表
    return schema.create()


if __name__ == '__main__':
    data = get_register_data(10)
    print(data)
    print(type(data))
    print(data[0])