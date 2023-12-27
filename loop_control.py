from read_yaml import Read_Config_Yaml, Read_CSV, Read_Phone_Camera_Config
from upload_playlst import Upload
# from set_blocksize import SetBlocksize
from down_bmp import DownBmp
from compare_image import CompareImage
from Webhook_send_msg import wenhook_for_loop,wenhook_send_error_playlist
from loop_log import logger

# 初始化函数导入
from initialize import initialize_folder,initialize_device

import time
import threading
import csv
import os

# 读取测试设备信息 是个列表
devicesdatas = Read_Config_Yaml().Devices_yaml()
# 读取是否拍照等配置
whether_data = Read_Phone_Camera_Config()
# 所需测试用例的名称
case_name = str(whether_data['case_name'])
wait_time = int(whether_data['wait_time'])

whether_camera = int(whether_data['whether_camera'])
save_or_contrast_bmp = int(whether_data['save_or_contrast_bmp'])
Fcms_version = int(whether_data['Fcms_version'])
whether_str_affirm = int(whether_data['whether_str_affirm'])
blocksize = int(whether_data['blocksize'])
save_bmp_url = str(whether_data['save_bmp_url'])

# 读播放表 是个列表
playlists = Read_CSV().Playlist_csv(case_name)

# # 拍照
# from Camera_OR_Video import Camera_OR_Video
#
# # ip与端口号
# from read_yaml import Read_host_port, Read_Phone_Camera_Config




def loop_control(device, item) :

    try:
        ip = device['device_ip']
        port = device['device_port']
        protocol = device['protocol']
        device_type = device['device_type']
        device_name = device['device_name']
        xstudio_version = device['xstudio_version']
        width = device['screen_width']
        height = device['screen_height']
        logger.info("%s %s %s %s %s %s %s %s", protocol, device_name, device_type, ip, port, xstudio_version, width,
                    height)

        # print(item)
        playlist_id, titles, playlist = item[0], item[3], item[4]
        logger.info("%s %s %s", playlist_id, titles, playlist)
        # 上载播放表
        res1 = Upload(ip = ip, port = port).upload(playlist = playlist)
        logger.warning("上载播放表结果 {}".format(res1))

        time.sleep(wait_time // 2)
        file_path = f'./picture/{device["device_type"]}/{device["xstudio_version"]}/{device["screen_width"]} {device["screen_height"]}'
        file_path1 = f'./picture/{device["device_type"]}/{device["xstudio_version"]}/{device["screen_width"]} {device["screen_height"]}/Now'

        if save_or_contrast_bmp == 0 :
            print("下载图片")
            logger.info("下载图片")
            DownBmp(ip = ip, port = port).downbmp("{0}/{1}.bmp".format(file_path, playlist_id))
            time.sleep(wait_time // 2)
            # if res1 == res2 == 1:
            #     return str(res1,res2)
            # else:
            #     return str(res1,res2)
        if save_or_contrast_bmp == 1 :
            logger.info("下载图片并对比")
            print("下载图片并对比")
            DownBmp(ip = ip, port = port).downbmp("{0}/{1}.bmp".format(file_path1, playlist_id))
            time.sleep(wait_time // 2)
            contrast_result = CompareImage().compare_image("{0}/{1}.bmp".format(file_path, playlist_id),
                                                           "{0}/{1}.bmp".format(file_path1, playlist_id).format(
                                                               playlist_id),
                                                           playlist_id)
            logger.warning("对比图片结果 {}".format(contrast_result))
            if contrast_result:
                print('图片对比通过')
            else:
                wenhook_send_error_playlist(device_name,playlist_id,titles,playlist)
    except Exception as e :
        logger.error("Error while {}".format(e))

def process_data(device, data) :
    for item in data :
        loop_control(device, item)  # 调用函数A并获取结果
        # print(device, item)

if __name__ == '__main__':
    wenhook_for_loop('开始测试')
    # 初始化文件夹
    initialize_folder()
    # 获取版本
    initialize_device()

    # 创建并启动线程
    threads = []
    for device in devicesdatas :
        t = threading.Thread(target = process_data, args = (device, playlists))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads :
        t.join()

    wenhook_for_loop('测试结束')

