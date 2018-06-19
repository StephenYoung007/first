import hashlib


origen_password = '^%&wang1314@@%'.encode('ascii')
pwd = hashlib.sha256(origen_password).hexdigest()
print(pwd)

for i in range(0,999999):
    p = str(i).zfill(6)
    # print(p)
    b = p.encode('ascii')
    password = hashlib.sha256(b).hexdigest()
    # print(password, p)
    if password == pwd:
        print('原密码是:',p)

print('====end====')


# 9e25d9e0feebb92178df70684721fdb041a0b0bb9148363d9e0f60a8cb7f3d09