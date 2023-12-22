from FcmsTool import FcmsTool
from read_yaml import Read_Phone_Camera_Config
from Set_log import logger
import socket

config_data = Read_Phone_Camera_Config()
blocksize = int(config_data['blocksize'])


class DownBmp(FcmsTool):
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.size = 1024

    def downbmp(self, bmp_url):
        try:
            # 帧类型
            frame_type1 = b'0'
            frame_type2 = b'9'
            # 帧尾
            frame_end = b'\03'
            down_name = 'currentframe.bmp'.encode('gbk')
            offset_count = 0
            picute_data = b''
            while True:
                offset = (self.size * offset_count).to_bytes(4, byteorder='big', signed=True)
                check_code_data = self.frame_addres1 + self.frame_addres2 + frame_type1 + frame_type2 + down_name + offset
                # crc检验
                check_code = self.crc16_xmodem(check_code_data.hex())

                data = down_name + offset
                data = self.send_byte(data)
                # 组合帧Data
                data = self.frame_headers + frame_type1 + frame_type2 + data + check_code + frame_end

                # result = ' '.join(data.hex()[i :i + 2] for i in range(0, len(data.hex()), 2))
                # logger.info(result)

                self.a.send(data)
                offset_count += 1
                # 1024收不完*2
                res = self.a.recv(self.size * 2)

                msg = self.reverse_byte(res)

                # result1 = ' '.join(msg.hex()[i :i + 2] for i in range(0, len(msg.hex()), 2))
                # logger.info(result1)

                # 若x70返回帧校验这里为msg[5 :-3]
                msg = msg[3:-3]
                picute_data += msg

                if len(res) < self.size and len(res) != 1460 and len(res) != 595 and len(res) != 1590:
                    with open(bmp_url, 'wb') as f:
                        f.write(picute_data)
                    logger.info('break')
                    break
        except Exception as e:
            logger.error("下载图片异常")
            logger.error(e)


if __name__ == "__main__":
    DownBmp(ip='202.11.11.1', port=2929).downbmp('./110.bmp')
