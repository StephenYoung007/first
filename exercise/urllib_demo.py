import urllib.parse

url = '%7B'

u = urllib.parse.unquote(url)

print(u)