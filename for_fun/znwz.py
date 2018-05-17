import requests
import os

num = 71
i=1
url_root = 'https://images.unsplash.com/photo-1494249465471-5655b7878482?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=191559dc1cae3f8967d568dfd8a77093&auto=format&fit=crop&w=800&q=60'
dir = str(url_root.split('/')[-2])
os.makedirs(dir)
while i < num:
    if i <10:
        index = '00' + str(i)
    elif i < 100:
        index = '0' + str(i)
    else:
        index = str(i)

    url_index = url_root + index
    url = url_index + 's.jpg'
    print(url)
    r = requests.get(url,stream=True)
    filename = str(i) + '.jpg'
    # path = url_index + '//'
    # file = './/' + path + filename
    with open('./' + dir + '/'+filename, 'wb') as fd:
        for chunk in r.iter_content():
            fd.write(chunk)
    i = i + 1

# 作者：爬虫
# 链接：https://www.zhihu.com/question/63503594/answer/209790574
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。