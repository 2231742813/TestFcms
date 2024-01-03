# coding=utf-8
import os
import yaml
import csv

yaml.warnings({'YAMLLoadWarning': False})

# 读取yaml文件


#  读取host与port
class Read_host_port:
    def Read(self):
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 拼接用例路径
        # case_path = project_path + '\Test_data' + '\host_port.yaml'
        case_path = './data/host_port.yaml'
        f = open(case_path, 'r', encoding='gbk')
        res = f.read()
        res = yaml.load(res)
        res = res['host_port']
        f.close()
        return res['host'], int(res['port'])

class Read_CSV :
    def Playlist_csv(self,case_name):
        csse_name = './data/{}'.format(case_name)
        print(csse_name)
        with open(csse_name, encoding='utf-8') as f:
            datas = list(csv.reader(f))
            return datas
# res = Read_CSV().Playlist_csv('x91_fcms.csv')
# for i in res:
#     print(i)

class Read_Config_Yaml :
    def Read_config_yaml(self):
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 拼接用例路径
        case_path = './data/config.yaml'
        f = open(case_path, 'r', encoding='utf-8')
        res1 = f.read()
        res1 = yaml.load(res1)
        f.close()
        return res1

    def Devices_yaml(self):
        with open('./data/Devices.yaml', mode = 'r', encoding = 'utf-8') as f :
            data = yaml.safe_load(f)
            f.close()
            return data

    def SSH_yaml(self):
        with open('./data/ssh.yaml', mode = 'r', encoding = 'utf-8') as f :
            data = yaml.safe_load(f)
            f.close()
            return data
# res = Read_Config_Yaml().SSH_yaml()
# print(res['hostname'])

# res = Read_Config_Yaml().Devices_yaml()
# for i in res:
#     print(i)

def Read_Phone_Camera_Config():
    with open('./data/Phone_Camera_Config.yaml', mode='r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        f.close()
        return data

