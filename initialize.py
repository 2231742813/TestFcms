from read_yaml import Read_Config_Yaml
from set_blocksize import SetBlocksize
import os
from Webhook_send_msg import wenhook_send_message
from A001_get_xstudio_version import GetXstudioVersion

devicesdatas = Read_Config_Yaml().Devices_yaml()


def initialize_folder() :
    for i in devicesdatas :
        # 将控制器Blocksize设为1024
        print(i['device_ip'],i['device_port'])
        SetBlocksize(ip = i['device_ip'], port = i['device_port']).setblocksize()
        file_path = f'./picture/{i["device_type"]}/{i["xstudio_version"]}/{i["screen_width"]} {i["screen_height"]}'
        os.makedirs(file_path, exist_ok = True)  # Create the directory and its parents if they don't exist
        open(file_path + '/Test image storage path.txt', 'w').close()  # Create a file within the directory

        file_path1 = f'./picture/{i["device_type"]}/{i["xstudio_version"]}/{i["screen_width"]} {i["screen_height"]}/Now'
        os.makedirs(file_path1, exist_ok = True)  # Create the directory and its parents if they don't exist
        open(file_path1 + '/Now image storage path.txt', 'w').close()  # Create a file within the directory

def initialize_device() :
    for i in devicesdatas :
        # 将控制器Blocksize设为1024

        res = GetXstudioVersion(ip = i['device_ip'],port = i['device_port']).get_xstudio_version()
        msg = "{0} {1}".format(i['device_name'],res)
        if res:
            wenhook_send_message(message = msg)
        else:
            wenhook_send_message(message = msg + 'Failed to get xstudio version')