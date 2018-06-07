import json


# list = []
# i = 1
# while i < 5 :
#     list.append(int(input('please input the element:')))
#     i += 1
#
# print(list)
# s = json.dumps(list, indent=2, ensure_ascii=False)
# with open('./save.txt', 'w') as f:
#     f.write(s)
with open('./save.txt', 'r') as f:
    s = f.read()

m = json.loads(s)
print(m)
print(type(m))
for ele in m:
    print(ele)
    print(type(ele))