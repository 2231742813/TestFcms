from apscheduler.schedulers.blocking import BlockingScheduler
import os
import time
from PIL import Image

from read_yaml import Read_Phone_Camera_Config
from Set_log import logger
from Send_Email import Send_Email
from Webhook_send_msg import Wenhook_send, Wenhook_send_video, Wenhook_send_1

data = Read_Phone_Camera_Config()
target_folder = data['target_folder']
# 是否发送邮件
whether_sendemail = int(data['whether_sendemail'])
# 是否开启企业微信内网机器人推送功能
whether_Webhook_url = int(data['whether_Webhook_url'])
# 是否开启企业微信机器人推送外网可看功能
Webhook_url_Wenhook_url_1 = int(data['Webhook_url_Wenhook_url_1'])


# 调用手机相机拍照或录屏并上传
def Camera_OR_Video(camera_or_video=0, wait_time=5, titles="默认标题", descriptions="playlists") :
    try :
        # 点亮手机
        os.system("adb shell input keyevent 224")
        time.sleep(1)
        # 解锁屏幕（前提需要在设置里面把手机登录的密码这些都关掉）
        os.system("adb shell input keyevent 82")
        time.sleep(1)
        # 清后台
        os.system("adb shell am kill-all")
        time.sleep(1)
        if camera_or_video == 0 :
            print("开始拍照")
            # 启动相机
            os.system("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA")
            # 多留点时间自动对焦
            time.sleep(3)
            # 按键27拍照
            os.system("adb shell input keyevent 27")
            # 留点时间存储照片防止读取到上一张图片
            time.sleep(5)
            # 获得最新的一张照片的文件名
            picture_url = os.popen("adb shell ls -t /storage/emulated/0/DCIM/Camera/ -t").read()
            # print(picture_url)
            name_list = picture_url.split("\n")
            # 若手机Camera文件下有一个缓存文件夹则用name_list[1]，没有则用name_list[0]
            myfilename = name_list[1]
        elif camera_or_video == 1 :
            print('开始录像')
            os.system("adb shell am start -a android.media.action.VIDEO_CAPTURE")
            # 多留点时间自动对焦
            time.sleep(2)
            # 开始录屏
            os.system("adb shell input keyevent 27")
            # 录屏时间
            time.sleep(wait_time)
            # 结束录屏
            os.system("adb shell input keyevent 27")
            time.sleep(10)
            os.system("adb shell input tap 900 102")
            time.sleep(10)
            # 获得最新的一张视频的文件名
            picture_url = os.popen("adb shell ls -t /storage/emulated/0/DCIM/Camera/ -t").read()
            # print(picture_url)
            name_list = picture_url.split("\n")
            # 若手机Camera文件下有一个缓存文件夹则用name_list[1]，没有则用name_list[0]
            myfilename = name_list[0]
        else :
            print("输入的内容错误，执行拍照操作")
            print("开始拍照")
            # 启动相机
            os.system("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA")
            # 多留点时间自动对焦
            time.sleep(3)
            # 按键27拍照
            os.system("adb shell input keyevent 27")
            # 留点时间存储照片防止读取到上一张图片
            time.sleep(5)
            # 获得最新的一张图片的文件名
            picture_url = os.popen("adb shell ls -t /storage/emulated/0/DCIM/Camera/ -t").read()
            # print(picture_url)
            name_list = picture_url.split("\n")
            # 若手机Camera文件下有一个缓存文件夹则用name_list[1]，没有则用name_list[0]
            myfilename = name_list[1]
        print("图片名称{}".format(myfilename))
        time.sleep(1)
        # 指定要保存到的目标文件夹路径,构建adb命令
        adb_code = "adb pull /storage/emulated/0/DCIM/Camera/" + myfilename + " " + target_folder
        # 执行adb命令
        os.system(adb_code)
        time.sleep(1)
        # back键 暂退相机
        os.system("adb shell input keyevent 4")
        time.sleep(1)
        # Power键 黑屏
        os.system("adb shell input keyevent 26")
        time.sleep(2)

        # 调用邮件发送图片至邮箱
        if whether_sendemail == 1:
            Send_Email(myfilename)
            logger.info("发送邮件功能开启")
            time.sleep(2)
        elif whether_sendemail == 0:
            logger.info("发送邮件功能关闭")
        else:
            logger.error('whether_sendemail参数异常')


        # 直接企业微信推送图片，仅内网可看
        if whether_Webhook_url == 1:
            Wenhook_send(myfilename, titles = titles, descriptions = descriptions)
            logger.info('企业微信内网推送开启')
        elif whether_Webhook_url == 0:
            logger.info('企业微信内网推送关闭')
        else:
            logger.error('whether_Webhook_url参数错误')



        # 压缩后直接企业微信推送图片，有网即可查看
        if Webhook_url_Wenhook_url_1 == 1:
            logger.info("企业微信外网推送开启")
            Wenhook_send_1(myfilename)
        elif Webhook_url_Wenhook_url_1 == 0:
            logger.info("企业微信外网推送关闭")
        else:
            logger.error('Webhook_url_Wenhook_url_1参数错误')

        # # 裁减图片之后内网推送
        # if camera_or_video == 0 :
        #     # Wenhook_send(myfilename, titles=titles, descriptions=descriptions)
        #     new_name = cute(myfilename)
        #     Wenhook_send(new_name, titles = titles, descriptions = descriptions)
        # elif camera_or_video == 1 :
        #     Wenhook_send_video(myfilename, titles = titles, descriptions = descriptions)
        # else :
        #     print("异常")

        return myfilename

    except Exception as e :
        print(F"Error{e}")


# Camera_OR_Video(camera_or_video=0, wait_time=10)
# 裁减云端图片
def cute(myfilename) :
    path = target_folder + myfilename
    img = Image.open(path)
    print("照片size：{}".format(str(img.size)))
    cropped = img.crop((0, 0, 3305, 3349))  # (left, upper, right, lower)
    new_url = target_folder + "cute" + myfilename
    new_name = "cute" + myfilename
    cropped.save(new_url)
    return new_name


# 处理时间，定时调手机拍照的
def photo_time(times=None) :
    times = times.split(",")
    scheduler = BlockingScheduler()
    for i in times :
        scheduler.add_job(Camera_OR_Video(), 'cron', day_of_week = None, hour = i[0 :2 :], minute = i[2 :4 :],
                          second = i[4 :6 :],
                          timezone = "Asia/Shanghai")
    scheduler.start()
