# coding=utf-8
import base64
import csv
import socket
import threading
import time
import wx
import yaml
from retrying import retry

# 图片对比
# crc校验
from CRC_16_XMODEM import crc16_xmodem
# 拍照
from Camera_OR_Video import Camera_OR_Video
# log
from Set_log import logger
from Webhook_send_msg import Wenhook_send_picuter_result
from compare_image import CompareImage
# ip与端口号
from read_yaml import Read_host_port, Read_Phone_Camera_Config

# 读取是否拍照配置
whether_data = Read_Phone_Camera_Config()
whether_camera = int(whether_data['whether_camera'])
save_or_contrast_bmp = int(whether_data['save_or_contrast_bmp'])
Fcms_version = int(whether_data['Fcms_version'])
whether_str_affirm = int(whether_data['whether_str_affirm'])
blocksize = int(whether_data['blocksize'])
save_bmp_url = str(whether_data['save_bmp_url'])
case_name = str(whether_data['case_name'])


class MaimFrame(wx.Frame):
    def __init__(self, parent, id):
        # ip初始化
        host, port = Read_host_port().Read()
        #
        wx.Frame.__init__(self, parent, id, title="TestFcms V1.0.1", pos=(100, 100), size=(860, 845))
        # self.SetMaxSize((860, 800))  # 设置最大窗口大小
        # self.SetMinSize((860, 800))  # 设置最小窗口大小 设置一样使其不能拉伸和缩小
        # 创建第一个面板ip,port
        panel = wx.Panel(self, pos=(0, 0), size=(160, 80))
        # ip,port静态文本框
        self.label_ip = wx.StaticText(panel, label="IP", pos=(5, 10))
        self.label_port = wx.StaticText(panel, label="port", pos=(5, 40))
        # ip,port,展示输入输入框
        self.text_ip = wx.TextCtrl(panel, pos=(40, 10), size=(100, 20), style=wx.TE_LEFT)
        self.text_port = wx.TextCtrl(panel, pos=(40, 40), size=(50, 20), style=wx.TE_LEFT)
        Confirm_button = wx.Button(panel, label='保存', pos=(100, 40), size=(45, 30))
        Confirm_button.Bind(wx.EVT_BUTTON, self.save_OnclickSubmit)
        # 设置默认值
        self.text_ip.SetValue(host)
        self.text_port.SetValue(str(port))

        # 创建第二个面板（----------------测试结果显示框-----------------------------）
        panel1 = wx.Panel(self, pos=(162, 0), size=(698, 800))
        self.show_text = wx.TextCtrl(panel1, id=-1, value='', pos=(0, 0), size=(680, 790),
                                     style=wx.TE_MULTILINE | wx.TE_READONLY)

        # 背景颜色
        self.show_text.SetOwnBackgroundColour('white')
        # 字体颜色
        self.show_text.SetOwnForegroundColour('#0d0e0c')

        # 创建第三个面板读取显示内容
        panel3 = wx.Panel(self, pos=(0, 82), size=(160, 80))
        self.Show_playlist_name = wx.StaticText(panel3, label="取情报板当前显示内容", pos=(5, 10))
        self.Show_playlist = wx.Button(panel3, label='读取', pos=(20, 35), size=(100, 30))
        self.Show_playlist.Bind(wx.EVT_BUTTON, self.test_get_device_show_content)

        # 创建第四个面板
        # 上载多个播放表
        panel4 = wx.Panel(self, pos=(0, 164), size=(160, 120))
        # 循环次数，循环英文Cycles
        self.Cycles = wx.StaticText(panel4, label="循环次数", pos=(5, 10))
        self.Cycles = wx.TextCtrl(panel4, pos=(70, 10), size=(50, 20), style=wx.TE_LEFT)
        self.Cycles.SetValue('1')
        self.interval_time = wx.StaticText(panel4, label="间隔时间(s)", pos=(5, 50))
        self.interval_time = wx.TextCtrl(panel4, pos=(70, 50), size=(50, 20), style=wx.TE_LEFT)
        self.interval_time.SetValue('30')
        # 上载按钮
        self.b1 = wx.ToggleButton(panel4, label='上载多个播放表', pos=(20, 80), size=(100, 30))
        self.Bind(wx.EVT_TOGGLEBUTTON, self.__on_click, self.b1)
        self.i = 0
        self.__stopped = True  # 此属性未使用
        self.running = False
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.b1, proportion=1, flag=wx.ALIGN_CENTRE_HORIZONTAL | wx.SHAPED | wx.BOTTOM, border=10)
        panel4.SetSizer(vbox)

        panel5 = wx.Panel(self, pos=(0, 285), size=(160, 80))
        self.tiaoshi = wx.Button(panel5, label='调试', pos=(20, 35), size=(100, 30))
        self.tiaoshi.Bind(wx.EVT_BUTTON, self.down_bmp)

    # 上载多个播放表
    @retry()
    def test_upload_playlists(self):
        # self.set_blocking()
        # host, port = Read_host_port().Read()
        host = str(self.text_ip.GetValue())
        port = int(self.text_port.GetValue())
        x = 2
        x = int(self.Cycles.GetValue())
        interval_time = int(self.interval_time.GetValue())

        while self.running:
            while x > 0:
                # 直接写死./data/datas.csv
                with open('./data/{}'.format(case_name), encoding='utf-8') as f:
                    datas = csv.reader(f)
                    for line in datas:
                        playlist_id, camera_or_video, wait_time, titles, playlists = line
                        logger.info("播放表信息 playlist_id, camera_or_video, wait_time, titles, playlists")
                        logger.info(line)

                        affirm_playlists = playlists
                        now = time.localtime()
                        now_time = time.strftime("[%m-%d %H:%M:%S]", now)
                        self.show_text.AppendText(
                            "----------------------------------------------------------------------------------------------------------------------------------\n")
                        # upload_count += 1
                        self.show_text.AppendText("{} 上载播放表\n".format(now_time))
                        self.show_text.AppendText("{0} 播放表格式：\n{1}\n".format(now_time, playlists))
                        logger.info("开始上载播放表")
                        logger.info("播放表格式：\n{}".format(playlists))
                        # 连接设备
                        socket.setdefaulttimeout(2)
                        a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        a.connect(tuple((host, port)))
                        # 帧头
                        frame_header = b'\x02'
                        # 地址
                        frame_addres1 = b'0'
                        frame_addres2 = b'0'
                        # 帧类型
                        frame_type1 = b'1'
                        frame_type2 = b'0'
                        # 帧数据,帧数据由三部分组成，文件名（data），分隔符（data1），文件指针偏移（data3），一段文件内容（data4）
                        data = 'play.lst'.encode('gbk')
                        s = data.hex()
                        check_code_data = data.hex()
                        data9 = base64.b16decode(s.upper())
                        data1 = b'\x2B'
                        check_code_data1 = data1.hex()
                        data6 = '\0\0\0\0'.encode('gbk')
                        data7 = playlists.encode('gbk')
                        data2 = data6 + data7
                        s2 = data2.hex()
                        check_code_data2 = data2.hex()
                        data2 = base64.b16decode(s2.upper())
                        # 校验码拼接,拼接后为字符串
                        check_code = (frame_addres1 + frame_addres2 + frame_type1 + frame_type2).hex() \
                                     + check_code_data + check_code_data1 + check_code_data2
                        # crc检验
                        check_code = crc16_xmodem(check_code)
                        # 转为字节，格式为'\x**\x**'
                        check_code = base64.b16decode(check_code.upper())
                        # 帧尾
                        frame_end = b'\03'
                        # 组合帧Data
                        data = frame_header + frame_addres1 + frame_addres2 + frame_type1 + frame_type2 + data9 + data1 + data2 + check_code + frame_end
                        logger.info("发送数据: {}".format(data.hex()))
                        # 发送数据
                        a.send(data)
                        # 接受返回数据
                        msg = a.recv(1024)
                        # 断开连接
                        a.close()
                        logger.info("接受数据: {}".format(msg.hex()))
                        now = time.localtime()
                        now_time = time.strftime("[%m-%d %H:%M:%S]", now)
                        self.show_text.AppendText(
                            "------等待{}s\n".format(interval_time / 2))
                        logger.info("-----------------------------------等待 {}s ")
                        time.sleep(interval_time / 2)
                        now = time.localtime()

                        if whether_camera == 1:
                            # 调用相机拍照
                            picture_name = Camera_OR_Video(camera_or_video=int(camera_or_video),
                                                           wait_time=int(wait_time), titles=titles,
                                                           descriptions=playlists)
                            self.show_text.AppendText(f"图片名称：{picture_name}\n")
                            self.show_text.write('拍照功能启用\n')
                            logger.info(f"图片名称：{picture_name}")
                        elif whether_camera == 0:
                            logger.info("拍照功能关闭")
                            self.show_text.write('拍照功能关闭\n')
                        else:
                            logger.error('whether_camera参数错误')

                        # version = self.get_version()
                        # print(version)
                        # version = int(version[0 :1 :])
                        # print(version)
                        # logger.info("大版本号： %s", version)

                        now = time.localtime()
                        now_time = time.strftime("[%m-%d %H:%M:%S]", now)

                        self.show_text.AppendText(
                            "{0} 开始取currentframe.bmp\n".format(now_time))

                        version = Fcms_version
                        logger.info("Fcms_version {}".format(version))
                        if save_or_contrast_bmp == 0:
                            if version == 2:
                                self.down_bmp(save_bmp_url + str(playlist_id) + '.bmp')
                                time.sleep(interval_time / 2)
                            elif version == 3:
                                self.down_bmp(save_bmp_url + str(playlist_id) + '.bmp')
                                time.sleep(interval_time / 2)
                            else:
                                logger.error('Fcms_version获取异常')
                        elif save_or_contrast_bmp == 1:
                            if version == 2:
                                self.down_bmp('./picture/test/{}.bmp'.format(playlist_id))
                                time.sleep(interval_time / 4)
                                # 2版本对比图片
                                contrast_result = CompareImage().compare_image(
                                    './picture/test/{}.bmp'.format(playlist_id),
                                    './picture/2/{}.bmp'.format(playlist_id), playlist_id)
                                if contrast_result == 1:
                                    self.show_text.write("2.X版本图片对比                成功\n")
                                    logger.info('2.X版本图片对比成功')
                                elif contrast_result == 0:
                                    self.show_text.write("2.X版本图片对比        失败\n")
                                    logger.warn('2.X版本图片对比失败')
                                    Wenhook_send_picuter_result(playlist_id, playlists)
                                else:
                                    self.show_text.write("2.X版本图片对比出现异常\n")
                                    logger.warn('2.X版本图片对比出现异常')
                                time.sleep(interval_time / 4)
                            elif version == 3:
                                self.down_bmp('./picture/test/{}.bmp'.format(playlist_id))
                                time.sleep(interval_time / 4)
                                # 3版本对比图片
                                contrast_result = CompareImage().compare_image(
                                    './picture/test/{}.bmp'.format(playlist_id),
                                    './picture/3/{}.bmp'.format(playlist_id), playlist_id)

                                if contrast_result == 1:
                                    self.show_text.write("3.X版本图片对比                成功\n")
                                    logger.info('3.X版本图片对比成功')
                                elif contrast_result == 0:
                                    self.show_text.write("3.X版本图片对比        失败\n")
                                    logger.warn('3.X版本图片对比失败')
                                    Wenhook_send_picuter_result(playlist_id, playlists)
                                else:
                                    self.show_text.write("3.X版本图片对比出现异常\n")
                                    logger.warn('3.X版本图片对比出现异常')
                                time.sleep(interval_time / 4)
                            else:
                                logger.error('文件对比出现异常异常')
                        else:
                            logger.error("save_or_contrast_bmp参数错误")

                        # 从X70下载bmp图片
                        # self.down_bmp('./picture/2/{}.bmp'.format(playlist_id))
                        # time.sleep(interval_time / 2)

                        if whether_str_affirm == 1:
                            now = time.localtime()
                            now_time = time.strftime("[%m-%d %H:%M:%S]", now)

                            affirm_msg = self.test_get_device_show_content(event=1)
                            affirm_playlists2 = affirm_playlists.split(',', 3)
                            affirm_playlists2 = affirm_playlists2[len(affirm_playlists2) - 1]
                            self.show_text.AppendText("{0} 上载的字符串 {1}\n".format(now_time, affirm_playlists2))
                            self.show_text.AppendText("{0} 当前显示字符串 {1}\n".format(now_time, affirm_msg))
                            affirm_playlists1 = affirm_playlists.split(',', 3)
                            affirm_playlists1 = affirm_playlists1[len(affirm_playlists1) - 1]
                            if affirm_playlists1 == affirm_msg:
                                self.show_text.AppendText("{} 断言           成功\n\n".format(now_time))
                            else:
                                self.show_text.AppendText("{} 断言      失败\n\n".format(now_time))
                            time.sleep(1)
                        elif whether_str_affirm == 0:
                            self.show_text.AppendText('字符串断言关闭\n')
                            logger.info('字符串断言关闭')
                        else:
                            logger.error('whether_str_affirm参数错误')

                        if not self.running:
                            break

                x -= 1
                if not self.running:
                    break
                else:
                    continue

    def __stopped(self):
        self.running = False

    # 发送进行转义
    def send_meaning(self, msg_bytes):
        # 发送转义
        msg_bytes = msg_bytes.replace(b'\x1b', b'\x1b\x00')
        msg_bytes = msg_bytes.replace(b'\x02', b'\x1b\xe7')
        msg_bytes = msg_bytes.replace(b'\x03', b'\x1b\xe8')
        return msg_bytes

    # 接受进行转义
    def reverse_meaning(self, msg_bytes):
        # 接受转义
        msg_bytes = msg_bytes.replace(b'\x1b\x00', b'\x1b')
        msg_bytes = msg_bytes.replace(b'\x1b\xe7', b'\x02')
        msg_bytes = msg_bytes.replace(b'\x1b\xe8', b'\x03')
        return msg_bytes

    def down_bmp(self, bmp_url):
        try:
            size = blocksize
            frame_header = b'\x02'
            # 地址
            frame_addres1 = b'0'
            frame_addres2 = b'0'
            # 帧类型
            frame_type1 = b'0'
            frame_type2 = b'9'
            # 帧尾
            frame_end = b'\03'
            down_name = 'currentframe.bmp'.encode('gbk')
            offset_count = 0
            picute_data = b''
            # host, port = Read_host_port().Read()
            host = str(self.text_ip.GetValue())
            port = int(self.text_port.GetValue())
            socket.setdefaulttimeout(10)
            a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a.connect(tuple((host, port)))
            while True:
                offset = (size * offset_count).to_bytes(4, byteorder='big', signed=True)
                check_code_data = frame_addres1 + frame_addres2 + frame_type1 + frame_type2 + down_name + offset
                # crc检验
                check_code = crc16_xmodem(check_code_data.hex())
                check_code = check_code.upper()
                if len(check_code) % 2 != 0:
                    check_code = '0' + check_code
                check_code = base64.b16decode(check_code)

                data = down_name + offset + check_code
                data = self.send_meaning(data)
                # 组合帧Data
                data = frame_header + frame_addres1 + frame_addres2 + frame_type1 + frame_type2 + data + frame_end
                a.send(data)
                offset_count += 1
                # 1024收不完*2
                res = a.recv(size * 2)
                msg = self.reverse_meaning(res)
                msg = msg[3:-3]
                picute_data += msg
                if len(res) < size:
                    with open(bmp_url, 'wb') as f:
                        f.write(picute_data)

                    self.show_text.write("下载图片完成  {}\n".format(bmp_url))
                    break
        except Exception as e:
            logger.error("下载图片异常")
            logger.error(e)

    def __on_click(self, event):
        """启动或停止线程"""
        self.i += 1
        if self.i % 2 != 0:
            self.running = True
            th = threading.Thread(target=self.test_upload_playlists)
            # th = threading.Thread(target = self.down_bmp('1.bmp'))
            th.start()
            self.b1.SetLabel('结束')
        else:
            self.running = False
            self.b1.SetLabel('上载多个播放表')

    # 取当前情报板显示的内容
    def test_get_device_show_content(self, event):
        # host, port = Read_host_port().Read()
        host = str(self.text_ip.GetValue())
        port = int(self.text_port.GetValue())
        socket.setdefaulttimeout(2)
        a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            a.connect(tuple((host, port)))
            frame_header = b'\x02'
            # 地址
            frame_addres1 = b'0'
            frame_addres2 = b'0'
            # 帧类型
            frame_type1 = b'9'
            frame_type2 = b'7'
            # 校验码拼接,拼接后为字符串
            check_code = (frame_addres1 + frame_addres2 + frame_type1 + frame_type2).hex()
            # crc检验
            check_code = crc16_xmodem(check_code)
            # # 转为字节，格式为'\x**\x**'
            check_code = base64.b16decode(check_code.upper())
            # 帧尾
            frame_end = b'\03'
            # 组合帧Data
            data = frame_header + frame_addres1 + frame_addres2 + frame_type1 + frame_type2 + check_code + frame_end
            # 发送数据
            logger.info("取可变信息标志的当前显示内容")
            logger.info("发送数据: {}".format(data.hex()))
            a.send(data)
            # 接受返回数据
            msg = a.recv(1024)

            # 断开连接
            a.close()
            # msg = msg.hex()
            logger.info("接受数据: {}".format(msg))
            msg = self.reverse_meaning(msg)
            msg = msg[3:-3:]
            msg = msg.decode('gbk')
            # # 断言
            # # 断开连接
            # a.close()
            # # msg = msg.hex()
            # logger.info("接受数据: {}".format(msg))
            # msg = msg[10 :-6 :]
            # msg = binascii.unhexlify(msg)
            # msg = msg.decode('gbk', 'ignore')
            # # # 断言
            now = time.localtime()
            now_time = time.strftime("[%m-%d %H:%M:%S]", now)
            # self.show_text.AppendText(
            #     "----------------------------------------------------------------------------------------------------------------------------------\n")
            self.show_text.AppendText("{} 取可变信息标志的当前显示内容\n".format(now_time))
            self.show_text.AppendText("{0} 返回信息为:{1}\n".format(now_time, msg))
            self.show_text.AppendText("{0} 播放序号 {1}\n".format(now_time, msg[0:3:]))
            logger.info("播放序号 {}".format(msg[0:3:]))
            self.show_text.AppendText("{0} 停留时间 {1}\n".format(now_time, msg[3:8:]))
            logger.info("停留时间 {}".format(msg[3:8:]))
            self.show_text.AppendText("{0} 出字方式 {1}\n".format(now_time, msg[8:10:]))
            logger.info("出字方式 {}".format(msg[8:10:]))
            self.show_text.AppendText("{0} 出字速度 {1}\n".format(now_time, msg[10:15:]))
            logger.info("出字速度 {}".format(msg[10:15]))
            self.show_text.AppendText("{0} 显示字符串 {1}\n".format(now_time, msg[15::]))
            logger.info("显示字符串 {}\n".format(msg[15::]))
            # self.show_text.AppendText(
            #     "------------------------------------
            a.close()
            return msg[14::]
        except Exception as e:
            logger.error(e)
            logger.error("获取情报板内容异常")

    # 获取版本号
    def get_version(self):
        try:
            # host, port = Read_host_port().Read()
            host = str(self.text_ip.GetValue())
            port = int(self.text_port.GetValue())
            # 连接X70
            logger.info("开始连接设备获取设备版本号")
            tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tn.connect(tuple((host, port)))
            # 通过套接字与X70建立连接
            frame_header = b'\02'  # 帧头
            frame_addres1 = b'0'  # 帧地址
            frame_addres2 = b'0'
            frame_type1 = b'9'  # 帧类型
            frame_type2 = b'9'
            frame_end = b'\03'  # 帧尾
            data = frame_addres1 + frame_addres2 + frame_type1 + frame_type2
            check_code = crc16_xmodem(data.hex())
            check_code = base64.b16decode(check_code.upper())
            data = frame_header + data + check_code + frame_end
            tn.send(data)
            m = tn.recv(1024)
            # print(m[1:-1:])
            msg = self.send_meaning(m[1:-1:])
            # print(msg)
            res = msg[2:-8].decode('utf-8')
            # print(res)
            res = res[11::]
            logger.info('返回的版本本 %s', res)
            return res
        except Exception as e:
            logger.error("获取版本号异常")
            logger.error(e)
            self.show_text.write("获取版本号异常\n")

    def set_blocking(self):
        try:
            X70_ip = self.text_ip.GetValue()
            port1 = int(self.text_port.GetValue())
            # 连接X70
            logger.info("连接设备")
            # self.show_text.write("连接设备\n")
            logger.info("设备IP及连接端口号：{} {}".format(X70_ip, port1))
            # self.show_text.write("设备IP及连接端口号：{} {}\n".format(X70_ip, port1))
            tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 通过套接字与X70建立连接
            tn.connect(tuple((X70_ip, port1)))
            frame_header = b'\x02'  # 帧头
            frame_addres1 = b'0'  # 帧地址
            frame_addres2 = b'0'
            frame_type1 = b'4'  # 帧类型
            frame_type2 = b'9'
            frame_end = b'\03'  # 帧尾
            data1 = '\0\1\0\0'.encode('gbk')
            # 将size转化为16进制   0800
            data2 = "{:0>4d}".format(eval(hex(1024)[2:]))
            data3 = base64.b16decode(data2.upper())  # 将16进制的size转化为b'\x**\x**'格式
            data = frame_addres1 + frame_addres2 + frame_type1 + frame_type2 + data1 + data3
            check_code = crc16_xmodem(data.hex())  # crc校验：b'\x41\x91'
            data4 = frame_header + data + check_code + frame_end
            logger.info("设置blocksize为1024")
            self.show_text.write("设置blocksize为1024\n")
            tn.send(data4)
            msg = tn.recv(1024)
            res = msg.hex()[6:8]
            code = chr(int(res, 16))
            if code == '0':
                # self.show_text.write('设置可变信息标志的blocksize成功\n')
                logger.info('设置可变信息标志的blocksize成功')
            else:
                # self.show_text.write('设置可变信息标志的blocksize失败\n')
                logger.error('设置可变信息标志的blocksize失败')
            # self.show_text.write('断开连接\n')
            logger.error('断开连接')
            tn.close()
        except Exception as e:
            # self.show_text.write('连接异常\n')
            logger.error("设置blocksize异常")
            logger.error(e)

    # 保存IP，port
    def save_OnclickSubmit(self, event):
        # 点击保存按钮
        host1 = self.text_ip.GetValue()
        port1 = self.text_port.GetValue()
        new_date = {
            'host_port': {
                "host": str(host1),
                "port": int(port1), }
        }
        f = open("./data/host_port.yaml", "w")
        yaml.dump(new_date, f)
        f.close()


def main():
    app = wx.App()
    win = MaimFrame(parent=None, id=-1)  # 创建窗体
    win.Show()  # 显示窗体
    app.MainLoop()  # 运行程序


if __name__ == "__main__":
    main()
