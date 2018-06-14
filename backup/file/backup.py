import os
import time

backup_time = time.strftime("%m%d%H%M%S", time.localtime())

def run():
    os.chdir('../')
    source_path = os.getcwd()
    dic = os.listdir(source_path)
    print('dic', dic)
    print(len(dic), type(dic))
    # i = 0
    gcode_list = []
    # if i < len(dic):
    #     if dic[i].find('.') != -1 and dic[i].split('.')[1] == 'gcode':
    #         gcode_list.append(dic[i])
    #         i += 1
    #     else:
    #         i +=1
    for ele in dic:
        if ele.find('.') != -1 and ele.split('.')[1] == 'gcode':
            gcode_list.append(ele)



    m = len(gcode_list)
    print('m', m)
    print(gcode_list)
    # while m != 0:
    #     print('gcode_list', gcode_list)
    #
    #     j = 0
    #     origen_path = 'F:\\3D打印备份\\' + backup_time + '\\'
    #     # os.mkdir(origen_path)
    #     print(origen_path)
        # for code in gcode_list:
        #     code_path = source_path + code
        #     print('code_path', code_path)
        #     with open(code_path, 'r', encoding='utf-8') as f:
        #         content = f.read()
        #         save_path = origen_path + code
        #         print(save_path)
        #         with open(save_path, 'w',encoding='utf-8') as new:
        #             new.write(content)
        #             readme_path = origen_path + 'readme.txt'
        #             with open(readme_path, 'w+') as s:
        #                 s.write(input('please input memorandum'))
        #                 s.close()
        #     os.remove(code_path)
        #     j = j + 1
        #     print('file {} copied'.format(code_path))

        # print(backup_time,j)

        # push test





if __name__ == '__main__':
    run()