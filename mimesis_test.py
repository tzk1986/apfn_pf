import requests

from mimesis import Person
from mimesis.schema import Schema

p = Person()
schema = Schema(
    schema=lambda: {
        'name': p.name(),
        'age': p.birthdate,
    }
)

data = schema.create()

print(data)

# data = {
#     'name': 'germey',
#     'age': '22'
# }



# res = requests.post(url='',data=data)
# print(res.json())
