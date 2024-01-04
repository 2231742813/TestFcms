from read_yaml import Read_Config_Yaml, Read_CSV, Read_Phone_Camera_Config
from upload_playlst import Upload
# from set_blocksize import SetBlocksize
from down_bmp import DownBmp
from compare_image import CompareImage
from Webhook_send_msg import wenhook_for_loop,wenhook_send_error_playlist,wenhook_for_error_pic
from loop_log import logger
# 初始化函数导入
from initialize import initialize_folder,initialize_device
from A004_handle_playlist import handle_playlist

import time
import threading
import os

# 读取测试设备信息 是个列表
devicesdatas = Read_Config_Yaml().Devices_yaml()
# 读取配置
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
error_pic_send_switch = int(whether_data['error_pic_send_switch'])
cut_the_length_playlist_head = int(whether_data['cut_the_length_playlist_head'])
cut_the_length_playlist_tail = int(whether_data['cut_the_length_playlist_tail'])
intervals_items = int(whether_data['intervals_items'])

# 读播放表 是个列表
playlists = Read_CSV().Playlist_csv(case_name)
# 裁剪播放列表
playlists = playlists[cut_the_length_playlist_head:cut_the_length_playlist_tail:]

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
        playlist_id, titles, playlist,whether_many_frame = item[0], item[3], item[4],item[5]
        logger.info("%s %s %s 此播放表是否多个播放项 %s", playlist_id, titles, playlist,whether_many_frame)
        # 上载播放表
        res1 = Upload(ip = ip, port = port).upload(playlist = playlist)
        logger.warning("上载播放表结果 {}".format(res1))
        time.sleep(2)
        # 是否存在多个播放项 0为只有一项 1为存在多项
        whether_many_frame = int(whether_many_frame)
        # print(whether_many_frame)
        # print(type(whether_many_frame))
        # print(wait_time)
        # print(save_or_contrast_bmp)
        if whether_many_frame == 0:
            time.sleep(wait_time // 2)
            file_path = f'./picture/{device["device_type"]}/{device["xstudio_version"]}/{device["screen_width"]} {device["screen_height"]}'
            file_path1 = f'./picture/{device["device_type"]}/{device["xstudio_version"]}/{device["screen_width"]} {device["screen_height"]}/Now'
            if save_or_contrast_bmp == 0 :
                print("下载图片")
                logger.info("下载图片")
                DownBmp(ip = ip, port = port).downbmp("{0}/{1}.bmp".format(file_path, playlist_id))
                time.sleep(wait_time // 2)
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
                if contrast_result :
                    print('图片对比通过')
                else :
                    wenhook_send_error_playlist(device_name, playlist_id, titles, playlist)
                    # 是否开启企业微信通知
                    if error_pic_send_switch == 1 :
                        wenhook_for_error_pic("{0}/{1}.bmp".format(file_path, playlist_id))
                        wenhook_for_error_pic("{0}/{1}.bmp".format(file_path1, playlist_id).format(playlist_id))
        if whether_many_frame == 1:
            pic_list = handle_playlist(playlist)
            timelist = [int(x) for x in pic_list]
            timelist = [x // 100 for x in timelist]
            jiange_time = 7
            num = 0
            newlist = [jiange_time]
            for i in range(len(timelist) - 1) :
                num = newlist[i] + timelist[i]
                # print(num)
                newlist.append(num)
            print(newlist)
            for i in range(len(newlist)) :
                if i == 0 :
                    waittime = newlist[i]
                else :
                    waittime = newlist[i] - newlist[i - 1] - 7
                print('等待下一个播放项 {}S'.format(waittime))

                if device["device_type"] == 'X70':
                    waittime = (intervals_items // 3) * 2
                else:
                    waittime = (intervals_items // 3) * 2
                time.sleep(waittime)
                file_path = f'./picture/{device["device_type"]}/{device["xstudio_version"]}/{device["screen_width"]} {device["screen_height"]}'
                file_path1 = f'./picture/{device["device_type"]}/{device["xstudio_version"]}/{device["screen_width"]} {device["screen_height"]}/Now'
                if save_or_contrast_bmp == 0 :
                    print("下载图片")
                    logger.info("下载图片")
                    DownBmp(ip = ip, port = port).downbmp("{0}/{1}-{2}.bmp".format(file_path, playlist_id,i))
                if save_or_contrast_bmp == 1 :
                    logger.info("下载图片并对比")
                    print("下载图片并对比")
                    DownBmp(ip = ip, port = port).downbmp("{0}/{1}-{2}.bmp".format(file_path1, playlist_id,i))
                    contrast_result = CompareImage().compare_image("{0}/{1}-{2}.bmp".format(file_path, playlist_id,i),
                                                                   "{0}/{1}-{2}.bmp".format(file_path1, playlist_id,i),
                                                                   playlist_id)
                    logger.warning("对比图片结果 {}".format(contrast_result))
                    if contrast_result :
                        print('图片对比通过')
                    else :
                        wenhook_send_error_playlist(device_name, playlist_id, titles, playlist)
                        # 是否开启企业微信通知
                        if error_pic_send_switch == 1 :
                            wenhook_for_error_pic("{0}/{1}-{2}.bmp".format(file_path, playlist_id,i))
                            wenhook_for_error_pic("{0}/{1}-{2}.bmp".format(file_path1, playlist_id,i))

    except Exception as e :
        logger.error("Error while {}".format(e))

def process_data(device, playlists) :
    for item in playlists :
        loop_control(device, item)  # 调用函数A并获取结果
        print(device, item)

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

