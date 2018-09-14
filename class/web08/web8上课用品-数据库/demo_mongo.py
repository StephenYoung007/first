import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017")

mongodb_name = 'web8'

db = client[mongodb_name]
db.authenticate('root', 'wy1314520')

import random

u = {
    'name': 'gua',
    'note': '瓜',
    # 放一个随机值来方便区分不同的数据以便下面的代码使用条件查询
    '随机值': random.randint(0, 3),
}
db.user.insert(u)

user_list = list(db.user.find())
print('所有用户', user_list)
