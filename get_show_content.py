from FcmsTool import FcmsTool
from Set_log import logger

# 取当前显示内容
class GetShowContent(FcmsTool) :

    def __init__(self, ip) :
        super().__init__(ip)

    def test_get_device_show_content(self) :
        # 帧类型
        frame_type1 = b'9'
        frame_type2 = b'7'
        # 校验码拼接,拼接后为字符串
        check_code = (self.frame_addres1 + self.frame_addres2 + frame_type1 + frame_type2).hex()
        # crc检验
        check_code = self.crc16_xmodem(check_code)

        # 组合帧Data
        data = self.frame_header + self.frame_addres1 + self.frame_addres2 + frame_type1 + frame_type2 + check_code + self.frame_end
        # 发送数据
        logger.info("取可变信息标志的当前显示内容")
        logger.info("发送数据: {}".format(data.hex()))
        self.a.send(data)
        # 接受返回数据
        msg = self.a.recv(1024)
        print(msg.hex())
        # 断开连接
        self.a.close()

        # msg = msg.hex()
        # logger.info("接受数据: {}".format(msg))
        # msg = self.reverse_meaning(msg)
        # msg = msg[3 :-3 :]
        # msg = msg.decode('gbk')
        #
        # # # # 断言
        # now = time.localtime()
        # now_time = time.strftime("[%m-%d %H:%M:%S]", now)
        # # self.show_text.AppendText(
        # #     "----------------------------------------------------------------------------------------------------------------------------------\n")
        # self.show_text.AppendText("{} 取可变信息标志的当前显示内容\n".format(now_time))
        # self.show_text.AppendText("{0} 返回信息为:{1}\n".format(now_time, msg[2 : :]))
        #
        # logger.info("返回信息为:{}".format(msg[2 : :]))
        # msg = msg[3 : :]
        # self.show_text.AppendText("{0} 播放序号 {1}\n".format(now_time, msg[0 :3 :]))
        # logger.info("播放序号 {}".format(msg[0 :3 :]))
        # self.show_text.AppendText("{0} 停留时间 {1}\n".format(now_time, msg[2 :7 :]))
        # logger.info("停留时间 {}".format(msg[2 :7 :]))
        # self.show_text.AppendText("{0} 出字方式 {1}\n".format(now_time, msg[7 :9 :]))
        # logger.info("出字方式 {}".format(msg[7 :9 :]))
        # self.show_text.AppendText("{0} 出字速度 {1}\n".format(now_time, msg[9 :14 :]))
        # logger.info("出字速度 {}".format(msg[9 :14 :]))
        # self.show_text.AppendText("{0} 显示字符串 {1}\n".format(now_time, msg[14 : :]))
        # logger.info("显示字符串 {}\n".format(msg[14 : :]))
        # # self.show_text.AppendText(
        # #     "------------------------------------
        # return msg[14 : :]


if __name__ == "__main__" :
    GetShowContent(ip = '202.11.11.55').test_get_device_show_content()
