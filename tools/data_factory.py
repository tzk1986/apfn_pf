from mimesis import Person
from mimesis.locales import Locale
from mimesis.schema import Schema
from mimesis import Address
import random


def get_register_data(x:int=1):
    """
    使用mimesis生成注册数据
    """
    p = Person(Locale.ZH)
    schema = Schema(
        schema=lambda: {
            'name': p.full_name(),
            'gender': p.gender(),
            'work': p.occupation(),
            'adress': Address(Locale.ZH).address(),
        },
        iterations=x)
    return schema.create()


if __name__ == '__main__':
    data = get_register_data(10)
    print(data)
    print(type(data ))
    print(data[0])