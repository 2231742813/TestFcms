from FcmsTool import FcmsTool
from Set_log import logger


class GetXstudioVersion(FcmsTool) :

    def __init__(self, ip,port) :
        super().__init__(ip)

    def get_xstudio_version(self) :

        try :
            # 帧类型
            frame_type1 = b'9'
            frame_type2 = b'9'
            # 校验码拼接,拼接后为字符串
            check_code = (self.frame_addres1 + self.frame_addres2 + frame_type1 + frame_type2).hex()
            # crc检验
            check_code = self.crc16_xmodem(check_code)

            # 组合帧Data
            data = self.frame_header + self.frame_addres1 + self.frame_addres2 + frame_type1 + frame_type2 + check_code + self.frame_end
            # 发送数据
            logger.info("取xstudio版本号")
            logger.info("发送数据: {}".format(data.hex()))
            self.a.send(data)
            # 接受返回数据
            msg = self.a.recv(1024)
            msg = self.reverse_byte(msg)
            res1 = msg[3 :-9].decode('utf-8')
            logger.error("get xstudio version success {0}".format(self.ip))
            return res1
        except Exception as e:
            logger.error("Could not get xstudio version Failed {0} {1}".format(e,self.ip))
            return 0

# if __name__ == "__main__" :
#     res = GetXstudioVersion(ip = '10.10.10.188',port = 2929).get_xstudio_version()
#     print(res)
