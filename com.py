# import re
# import socket
# import time
# import base64
# import os
# from binascii import unhexlify
# from crcmod import mkCrcFun
# # 下载图片使用
# #公共类
# class COM:
#
#     def __init__(self,ip,port=2929):
#         self.ip = ip
#         self.port = int(port)
#         socket.setdefaulttimeout(2.5)                     #设置超时连接时间
#         self.a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 通过套接字与X70建立连接
#         self.a.connect((self.ip, self.port))
#
#     def __del__(self):
#         self.a.close()                                              #类执行结束断开连接
#
#
#     def byte_change(self,st):                               #st为字节数据
#         st = st.replace(b'\x1b', b'\x1b\x00')        # 0x02转换为0x1B,0xE7  0x03转换为0x1B,0xE8   0x1B转换为0x1B,0x00
#         st = st.replace(b'\x02', b'\x1b\xe7')
#         st = st.replace(b'\x03', b'\x1b\xe8')
#         return st
#
#     def reverse_byte(self,m):
#         m = m.replace(b'\x1b\x00', b'\x1b')             # 字节数据反转
#         m = m.replace(b'\x1b\xe7', b'\x02')
#         m = m.replace(b'\x1b\xe8', b'\x03')
#         return m
#
#     # CRC16/XMODEM
#     def crc16_xmodem(self,data):
#         data = str(data)
#         crc16 = mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)
#         check_code = self.get_crc_value(data, crc16)            #进行16进制CRC校验
#         check_code = check_code.zfill(4)                        #不足4位补0
#         check_code1 = base64.b16decode(check_code.upper())      #check_code转为字节，例如将'caab'格式为'\xca\xab'
#         check_code2 = self.byte_change(check_code1)             #转化特殊字节数据
#         # print(check_code2.hex())
#         return check_code2
#
#     # common func
#     def get_crc_value(self,s, crc16):
#         data = s.replace(' ', '')
#         crc_out = hex(crc16(unhexlify(data))).upper()
#         str_list = list(crc_out)
#         if len(str_list) == 5:
#             str_list.insert(2, '0')
#         crc_data = ''.join(str_list[2:])
#         return (crc_data[:2] + crc_data[2:]).lower()
#
#     def get_time(self):
#         now = time.localtime()
#         now_time = time.strftime("[%m-%d %H:%M:%S]", now)
#         return now_time
#
#     def sleep(self,s):
#         time.sleep(s)
#
#     def write(self,data):
#         with open('down_bmp.log', mode='a+', encoding='utf-8') as f:     #a+表示追加写入
#             f.write(f'{data}\n')
#
#     def data_16(self,data):                 #将'0230303031caab03'输出 --> 02 30 30 30 31 CA AB 03
#         return ' '.join(re.findall("\w{2}",data.upper()))
#
#     def read_csv(self,file):
#         with open(file) as f:
#             l =  f.read().split('"')
#             l1 = list(i for i in l if (i!='\n') & (i !=''))
#         return l1
#
#     def read_txt(self,file):
#         with open(file,encoding='utf-8') as f:
#             s = f.read()
#         return s
#
#     def write_data(self,data,file):                           #将数据写入文件，从头写入，之前的删除
#         with open(file, mode='w', encoding='utf-8') as f:     #w表示写入
#             f.write(data)
#
#     def read_asbyte(self,file):                               #读取文件作为二进制
#         with open(file, 'rb') as f:
#             m = f.read()
#         return m
#
# #
# # if __name__ == '__main__':
# #
# #     c = COM('192.168.1.100')
# #
# #     # dd = c.read_txt('../log/senddata.log')
# #     # print(dd)
# #     # c.write('1')
# #     print(os.getcwd())
#
#
#     # print(c.data_16("0230303031caab03"))
#     # f = c.read_csv('../data/play.csv')
#     # print(f)
#     # res = c.read_txt('../data/play_1.txt')
#     # print(res)
#     # s = c.get_path()
#     # print(s)
#     # res = c.read_asbyte('../data/pic/D27.gif')
#     # print(len(res))
#     # s = b'\x02\x03\x1b\x04'
#     # st = c.byte_change(s)
#     # print(st)
#     # print(type(st))
#
#     # s = b'\xb9_'
#     # st = s.replace(b'\x03', b'\x1b\xe8')
#     # print(st)
#
#     # with open('../data/pic/' + '123.png', 'rb') as f:
#     #     m = f.read()
#     #     print(len(m))
#     #     s = c.byte_change(m)
#     #     print(len(s))
#     #     q = re.findall('x02',str(s))
#     #     print(q)
#     #     q = re.findall('x03',str(s))
#     #     print(q)
#     #     q = re.findall('x1b',str(s))
#     #     print(q)
#     #     print(len(q))
