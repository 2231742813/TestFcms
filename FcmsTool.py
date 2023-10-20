import re
import socket
import time
import base64
import os
from binascii import unhexlify
from crcmod import mkCrcFun
from Set_log import logger


# 公共类
class FcmsTool :

    def __init__(self, ip='202.11.11.1', port=2929, outtime=2.5) :
        try :
            self.ip = ip
            self.port = int(port)
            socket.setdefaulttimeout(outtime)  # 设置超时连接时间
            self.a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 通过套接字与X70建立连接
            self.a.connect((self.ip, self.port))

            self.frame_header = b'\x02'
            # 地址
            self.frame_addres1 = b'0'
            self.frame_addres2 = b'0'
            # 帧尾
            self.frame_end = b'\03'

            self.frame_headers = self.frame_header + self.frame_addres1 + self.frame_addres2
        except Exception as e :
            logger.error(e)
            logger.error("连接异常")

    def __del__(self) :
        logger.info("__del__")
        self.a.close()

    def send_byte(self, st) :  # st为字节数据
        st = st.replace(b'\x1b', b'\x1b\x00')  # 0x02转换为0x1B,0xE7  0x03转换为0x1B,0xE8   0x1B转换为0x1B,0x00
        st = st.replace(b'\x02', b'\x1b\xe7')
        st = st.replace(b'\x03', b'\x1b\xe8')
        return st

    def reverse_byte(self, m) :
        m = m.replace(b'\x1b\x00', b'\x1b')  # 字节数据反转
        m = m.replace(b'\x1b\xe7', b'\x02')
        m = m.replace(b'\x1b\xe8', b'\x03')
        return m

    # CRC16/XMODEM
    def crc16_xmodem(self, data) :
        data = str(data)
        crc16 = mkCrcFun(0x11021, rev = False, initCrc = 0x0000, xorOut = 0x0000)
        check_code = self.get_crc_value(data, crc16)  # 进行16进制CRC校验
        check_code = check_code.zfill(4)  # 不足4位补0
        check_code1 = base64.b16decode(check_code.upper())  # check_code转为字节，例如将'caab'格式为'\xca\xab'
        check_code2 = self.send_byte(check_code1)  # 转化特殊字节数据
        # print(check_code2.hex())
        # 返回字节
        return check_code2

    # common func
    def get_crc_value(self, s, crc16) :
        data = s.replace(' ', '')
        crc_out = hex(crc16(unhexlify(data))).upper()
        str_list = list(crc_out)
        if len(str_list) == 5 :
            str_list.insert(2, '0')
        crc_data = ''.join(str_list[2 :])
        return (crc_data[:2] + crc_data[2 :]).lower()

    def get_time(self) :
        now = time.localtime()
        now_time = time.strftime("[%m-%d %H:%M:%S]", now)
        return now_time

    def sleep(self, s) :
        time.sleep(s)

    def write(self, data) :
        with open('senddata.log', mode = 'a+', encoding = 'utf-8') as f :  # a+表示追加写入
            f.write(f'{data}\n')

    def data_16(self, data) :  # 将'0230303031caab03'输出 --> 02 30 30 30 31 CA AB 03
        return ' '.join(re.findall("\w{2}", data.upper()))
