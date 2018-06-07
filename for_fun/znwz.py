import requests
import os

num = 92
i=1
url_root = 'http://www.znwz.org/wp-content/uploads/2017/07/1I34V144-'   http://www.znwz.org/wp-content/uploads/2017/07/1I34TT3-11.jpg
dir = str(url_root.split('/')[-2])
os.makedirs(dir)
while i <= num:
    index = str(i)#.zfill(3)
    url_index = url_root + index
    url = url_index + '.jpg'
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