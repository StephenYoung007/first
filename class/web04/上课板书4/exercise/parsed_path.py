def parsed_path(path):
    index = path.find("?")
    if index == -1:
       new_path, query = path, {}
    else:
        new_path, query_string = path.split("?", 1)
        args = query_string.split("&")
        query = {}
        for arg in args:
            k, v = arg.split("=")
            query[k] = v
    return new_path, query

def run():
    test_args = {
        'www.baidu.con?name=yang',
        'hshshs.hhdh.com'
        'www.stephenyoung.top?name=stephenyoung&password=wy1314520'
    }
    for ele in test_args:
        a, b = parsed_path(ele)
        print(a, b)

if __name__ == '__main__':
    run()
