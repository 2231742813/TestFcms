import paramiko
import os
from read_yaml import Read_Config_Yaml
from Set_log import logger

# ssh上载bin升级文件   未通 失败  上传失败

# 读取ssh.yaml
res = Read_Config_Yaml().SSH_yaml()
device_datas = Read_Config_Yaml().Devices_yaml()

port = res['port']
username = res['username']
password = res['password']
bin_path = res['bin_path']


def upload_file() :
    try :
        for device in device_datas :
            if device['device_type'] == 'X90' :
                print(device)
                # x90升级
                directory = './bin'
                # 列出目录下的所有文件
                file_list = os.listdir(directory)
                bin_name = []
                # 遍历文件列表，找到符合条件的文件
                for file in file_list :
                    if "rk3399" in file and file.endswith(".bin") :
                        bin_name.append(file)
                if bin_name :
                    print(bin_name[0])
                    # 上传本地文件到远程Ubuntu系统
                    local_path = './bin/{}'.format(bin_name[0])
                    remote_path = bin_path
                    # 建立SSH连接,上传文件
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    logger.info(
                        "%s %s %s %s %s %s" % (device['device_ip'], username, password, port, local_path, remote_path))
                    try :
                        ssh.connect(device['device_ip'], username = username, password = password, port = port)
                        # 创建SFTP客户端
                        sftp = ssh.open_sftp()
                        sftp.put(local_path, remote_path)
                        # 关闭SFTP客户端和SSH连接
                        sftp.close()
                        ssh.close()
                    except Exception as e :
                        logger.error("An error occurred: %s" % str(e))

            if device['device_type'] == 'X91' :
                # x91升级
                pass

    except Exception as e :
        print("Error uploading file {}".format(e))
        logger.error("Error uploading file {}".format(e))


upload_file()
