from read_yaml import Read_Config_Yaml
from set_blocksize import SetBlocksize
import os
from Webhook_send_msg import wenhook_send_message
from A001_get_xstudio_version import GetXstudioVersion

devicesdatas = Read_Config_Yaml().Devices_yaml()


def create_directory(path):
    os.makedirs(path, exist_ok=True)  # Create the directory and its parents if they don't exist
    open(os.path.join(path, '测试图片路径.txt'), 'w').close()  # Create a file within the directory

def create_subdirectories(path):
    create_directory(path)
    now_path = os.path.join(path, 'Now')
    create_directory(now_path)
    os.makedirs(os.path.join(now_path, 'different_bak'), exist_ok=True)  # Create the directory and its parents if they don't exist
    open(os.path.join(now_path, 'different_bak', '测试异常的图片备份目录.txt'), 'w').close()  # Create a file within the directory
    return now_path

def delete_bmp_files(path):
    for file in os.listdir(path):
        if file.endswith(".bmp"):
            file_path = os.path.join(path, file)
            os.remove(file_path)

def initialize_folder():
    for i in devicesdatas:
        file_path = os.path.join('./picture', str(i["device_type"]), str(i["xstudio_version"]), f'{i["screen_width"]} {i["screen_height"]}')
        now_path = create_subdirectories(file_path)
        delete_bmp_files(now_path)

initialize_folder()





def initialize_device() :
    for i in devicesdatas :
        # 将控制器Blocksize设为1024
        print(i['device_ip'], i['device_port'])
        SetBlocksize(ip = i['device_ip'], port = i['device_port']).setblocksize()

        res = GetXstudioVersion(ip = i['device_ip'],port = i['device_port']).get_xstudio_version()
        msg = "{0} {1}".format(i['device_name'],res)
        if res:
            wenhook_send_message(message = msg)
        else:
            wenhook_send_message(message = msg + 'Failed to get xstudio version')

