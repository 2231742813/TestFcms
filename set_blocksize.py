from FcmsTool import FcmsTool
from Set_log import logger
import base64


class SetBlocksize(FcmsTool) :
    def __init__(self, ip='202.11.11.1', port=2929) :
        super().__init__(ip, port)
        self.size = 1024

    def setblocksize(self) :
        try :
            logger.info("设备IP及连接端口号：{} {}".format(self.ip, self.port))
            # 帧类型
            frame_type1 = b'4'
            frame_type2 = b'9'

            data1 = '\0\1\0\0'.encode('gbk')
            # 将size转化为16进制   0800
            data2 = "{:0>4d}".format(eval(hex(self.size)[2 :]))
            # 将16进制的size转化为b'\x**\x**'格式
            data3 = base64.b16decode(data2.upper())

            data = self.frame_addres1 + self.frame_addres2 + frame_type1 + frame_type2 + data1 + data3
            check_code = self.crc16_xmodem(data.hex())

            data4 = self.frame_header + data + check_code + self.frame_end

            self.a.send(data4)
            msg = self.a.recv(self.size)

            res = msg.hex()[6 :8]
            code = chr(int(res, 16))
            if code == '0' :
                logger.info('设置可变信息标志的blocksize成功 %s' % self.size)
            else :
                logger.error('设置可变信息标志的blocksize失败 %s' % self.size)
        except Exception as e :
            logger.error("设置blocksize异常")
            logger.error(e)


# if __name__ == '__main__' :
#     SetBlocksize(ip = '202.11.11.3', port = 2929).setblocksize()
