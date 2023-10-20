# coding=utf-8
import os
import yaml

yaml.warnings({'YAMLLoadWarning': False})


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
        return res['host'], int(res['port'])


class Read_Config_Yaml():
    def Read_config_yaml(self):
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 拼接用例路径
        case_path = './data/config.yaml'
        f = open(case_path, 'r', encoding='utf-8')
        res = f.read()
        res = yaml.load(res)
        return res



def Read_Phone_Camera_Config():
    with open('./data/Phone_Camera_Config.yaml', mode='r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        f.close()
        return data

