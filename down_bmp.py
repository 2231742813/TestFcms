from FcmsTool import FcmsTool
from read_yaml import Read_Phone_Camera_Config
from log_for_down import logger
from Webhook_send_msg import wenhook_send_error_playlist

config_data = Read_Phone_Camera_Config()
blocksize = int(config_data['blocksize'])


class DownBmp(FcmsTool) :
    def __init__(self, ip, port) :
        super().__init__(ip, port)
        logger.info("下载bmp 控制器信息：%s %s" % (ip, port))
        self.size = 1024

    def downbmp(self, bmp_url) :
        try :
            # 帧类型
            frame_type1 = b'0'
            frame_type2 = b'9'
            # 帧尾
            frame_end = b'\03'
            down_name = 'currentframe.bmp'.encode('gbk')
            offset_count = 0
            picute_data = b''
            while True :
                offset = (self.size * offset_count).to_bytes(4, byteorder = 'big', signed = True)
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
                msg = msg[3 :-3]
                picute_data += msg

                if len(res) < self.size and len(res) != 1460 and len(res) != 595 and len(res) != 1590 :
                    with open(bmp_url, 'wb') as f :
                        f.write(picute_data)

                    logger.info('触发break 下载完成')
                    break
        except Exception as e :
            wenhook_send_error_playlist('error下载图片异常\n', str(self.ip), str(self.port),str(bmp_url))
            logger.error("下载图片异常")
            logger.error(e)


# if __name__ == "__main__" :
#     DownBmp(ip = '10.10.10.170', port = 2929).downbmp('./1.bmp')

# from FcmsTool import FcmsTool
# from read_yaml import Read_Phone_Camera_Config
# from log.log_for_down import logger
# import socket
# config_data = Read_Phone_Camera_Config()
# blocksize = int(config_data['blocksize'])
# class DownBmp(FcmsTool):
#     def __init__(self, ip, port):
#         super().__init__(ip, port)
#         logger.info(" %s: %s" % (ip, port))
#         self.size = 1024
#
#     def downbmp(self, bmp_url):
#         try:
#             success = False  # Variable to track the success of the operation
#             # 帧类型
#             frame_type1 = b'0'
#             frame_type2 = b'9'
#             # 帧尾
#             frame_end = b'\03'
#             down_name = 'currentframe.bmp'.encode('gbk')
#             offset_count = 0
#             picute_data = b''
#             while True:
#                 offset = (self.size * offset_count).to_bytes(4, byteorder='big', signed=True)
#                 check_code_data = self.frame_addres1 + self.frame_addres2 + frame_type1 + frame_type2 + down_name + offset
#                 # crc检验
#                 check_code = self.crc16_xmodem(check_code_data.hex())
#
#                 data = down_name + offset
#                 data = self.send_byte(data)
#                 # 组合帧Data
#                 data = self.frame_headers + frame_type1 + frame_type2 + data + check_code + frame_end
#
#                 # result = ' '.join(data.hex()[i :i + 2] for i in range(0, len(data.hex()), 2))
#                 # logger.info(result)
#
#                 self.a.send(data)
#                 offset_count += 1
#                 # 1024收不完*2
#                 res = self.a.recv(self.size * 2)
#
#                 msg = self.reverse_byte(res)
#
#                 # result1 = ' '.join(msg.hex()[i :i + 2] for i in range(0, len(msg.hex()), 2))
#                 # logger.info(result1)
#
#                 # 若x70返回帧校验这里为msg[5 :-3]
#                 msg = msg[3:-3]
#                 picute_data += msg
#
#                 if len(res) < self.size and len(res) != 1460 and len(res) != 595 and len(res) != 1590 :
#                     with open(bmp_url, 'wb') as f :
#                         f.write(picute_data)
#                     logger.info('break')
#                     success = True  # Set success to True if the operation is successful
#                     break  # Exit the loop if the condition is met
#                 if success :
#                     logger.info('下载图片success')
#                     return 1  # Return 1 for successful execution
#                 else :
#                     return 0  # Return 0 if the loop completes without meeting the success condition
#         except Exception as e:
#             logger.error("下载图片Failed")
#             logger.error(e)
#             return 0
# if __name__ == "__main__":
#     DownBmp(ip='10.10.10.188', port=2929).downbmp('./1.bmp')


# from com import *
#
#
# class DownBmp(COM) :
#     ddd = ''
#     data2 = '\0\0\0\0'.encode('gbk')  # 文件指针偏移
#     ccc = b''
#     i = 1
#
#     def __init__(self, ip, port=2929) :
#         super().__init__(ip, port)  # 使用super对父类的被覆盖的方法进行调用
#         self.size = 1024
#
#     def download_file(self, file_name) :
#         frame_header = b'\02'  # 帧头
#         frame_addres1 = b'0'  # 帧地址
#         frame_addres2 = b'0'
#         frame_type1 = b'0'  # 帧类型
#         frame_type2 = b'9'
#         frame_end = b'\03'  # 帧尾
#         data1 = file_name.encode('gbk')
#         data = frame_addres1 + frame_addres2 + frame_type1 + frame_type2 + data1 + self.data2
#         check_code = self.crc16_xmodem(data.hex())  # crc校验
#         data3 = self.byte_change(self.data2)  # 特殊字节转化
#         data = frame_header + frame_addres1 + frame_addres2 + frame_type1 + frame_type2 + data1 + data3 + check_code + frame_end
#         self.a.send(data)
#         msg1 = self.a.recv(self.size * 2)
#         if len(msg1) == 1460 :  # 由于socket的recv接收数据限制，数据量大于1460时，大概率接收1460个字节就阻塞，故增加for循环，使之继续接收
#             for j in range(self.size // 1460) :
#                 msg2 = self.a.recv(self.size * 2)
#                 msg1 += msg2
#                 if len(msg2) != 1460 :
#                     break
#         msg = self.reverse_byte(msg1)  # 特殊字节反转
#         if file_name in ['current.json', 'play.lst'] :  # 'currentframe.bmp'文件的日志太多,选择不输出
#             self.write(f'{self.get_time()} send data({self.i}): ')
#             self.write(self.data_16(data.hex()))
#             self.write('receive data: ')
#             self.write(self.data_16(msg1.hex()))
#         if file_name == 'play.lst' :
#             self.ddd += msg[3 :-3].decode('gbk')
#             self.ddd = self.ddd.replace('\r', '')
#         elif file_name == 'current.json' :
#             if len(msg[3 :-3].hex()) / 2 == self.size :  # 接收的数据 = blocksize 继续接收
#                 self.ddd += msg[3 :-3].decode('utf-8')
#                 d1 = int(('0x' + self.data2.hex()), 16) + self.size  # 文件偏移指针+size并转化
#                 d2 = hex(d1)[2 :].zfill(8)  # zfill——字符串向前补0
#                 self.data2 = base64.b16decode(d2.upper())
#                 self.i += 1
#                 self.download_file(file_name)  # 递归，再次发送接受
#             else :
#                 self.ddd += msg[3 :-3].decode('utf-8')
#         elif file_name == 'currentframe.bmp' :
#             if len(msg[3 :-3].hex()) / 2 == self.size :
#                 self.ccc += msg[3 :-3]
#                 d1 = int(('0x' + self.data2.hex()), 16) + self.size  # 文件偏移指针+size并转化
#                 d2 = hex(d1)[2 :].zfill(8)  # zfill——字符串向前补0
#                 self.data2 = base64.b16decode(d2.upper())
#                 self.i += 1
#                 self.download_file(file_name)  # 递归
#             else :
#                 self.ccc += msg[3 :-3]
#
#     def downbmp(self, path,file_name='currentframe.bmp') :
#         self.write('----------------------------------------------------')  # 写入日志
#         self.write(f'{self.get_time()} 开始从可变信息标志下载文件{file_name} ... ...')
#         self.download_file(file_name)
#         if file_name == 'current.json' :
#             self.write_data(self.ddd, path)  # 写入文件
#         elif file_name == 'play.lst' :
#             self.write_data(self.ddd, path)
#         elif file_name == 'currentframe.bmp' :
#             with open(path, 'wb') as f :
#                 f.write(self.ccc)
#         self.write(f'{self.get_time()} 从可变信息标志下载文件 {file_name} 成功')
#         self.write(f'{self.get_time()} 文件保存在 {path}')
#
#
# # if __name__ == '__main__' :
# #     DownBmp('10.10.10.188',port = 2929).downbmp('./123/4.bmp')
#
# # DownBmp(ip='10.10.10.188', port=2929).downbmp('./1.bmp')


# from FcmsTool import FcmsTool
# from read_yaml import Read_Phone_Camera_Config
# from Set_log import logger
# import socket
#
# config_data = Read_Phone_Camera_Config()
# blocksize = int(config_data['blocksize'])
#
#
# class DownBmp(FcmsTool):
#     def __init__(self, ip, port):
#         super().__init__(ip, port)
#         self.size = 1024
#
#     def downbmp(self, bmp_url):
#         try:
#             # 帧类型
#             frame_type1 = b'0'
#             frame_type2 = b'9'
#             # 帧尾
#             frame_end = b'\03'
#             down_name = 'currentframe.bmp'.encode('gbk')
#             offset_count = 0
#             picute_data = b''
#             while True:
#                 offset = (self.size * offset_count).to_bytes(4, byteorder='big', signed=True)
#                 check_code_data = self.frame_addres1 + self.frame_addres2 + frame_type1 + frame_type2 + down_name + offset
#                 # crc检验
#                 check_code = self.crc16_xmodem(check_code_data.hex())
#
#                 data = down_name + offset
#                 data = self.send_byte(data)
#                 # 组合帧Data
#                 data = self.frame_headers + frame_type1 + frame_type2 + data + check_code + frame_end
#
#                 # result = ' '.join(data.hex()[i :i + 2] for i in range(0, len(data.hex()), 2))
#                 # logger.info(result)
#
#                 self.a.send(data)
#                 offset_count += 1
#                 # 1024收不完*2
#                 res = self.a.recv(self.size * 2)
#
#                 msg = self.reverse_byte(res)
#
#                 # result1 = ' '.join(msg.hex()[i :i + 2] for i in range(0, len(msg.hex()), 2))
#                 # logger.info(result1)
#
#                 # 若x70返回帧校验这里为msg[5 :-3]
#                 msg = msg[3:-3]
#                 picute_data += msg
#
#                 if len(res) < self.size and len(res) != 1460 and len(res) != 595 and len(res) != 1590:
#                     with open(bmp_url, 'wb') as f:
#                         f.write(picute_data)
#                     logger.info('break')
#
#                     break
#         except Exception as e:
#             logger.error("下载图片异常")
#             logger.error(e)
#             return 0
#
#
# # if __name__ == "__main__":
#     # DownBmp(ip='10.10.10.188', port=2929).downbmp('./0.bmp')
