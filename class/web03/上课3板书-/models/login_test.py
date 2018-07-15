import json
import os

with open("../db/User.txt", 'r', encoding='utf-8') as f:
    s = f.read()
    # print(s)
    print(type(s))
    print("-----------------------------------------")
    data = json.dumps(s, sort_keys=True)
    print(data)
    print(type(data))
    print(data.find('username'))