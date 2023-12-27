
from com import *

class Get_File(COM):

    ddd = ''
    data2 = '\0\0\0\0'.encode('gbk')                    #文件指针偏移
    ccc = b''
    i = 1

    def __init__(self, ip,port=2929):
        super().__init__(ip,port)                        #使用super对父类的被覆盖的方法进行调用
        self.size = 1024

    def download_file(self,file_name):
        frame_header = b'\02'                       # 帧头
        frame_addres1 = b'0'                        # 帧地址
        frame_addres2 = b'0'
        frame_type1 = b'0'                          # 帧类型
        frame_type2 = b'9'
        frame_end = b'\03'                          # 帧尾
        data1 = file_name.encode('gbk')
        data = frame_addres1 + frame_addres2 + frame_type1 + frame_type2 + data1 + self.data2
        check_code = self.crc16_xmodem(data.hex())                      #crc校验
        data3 = self.byte_change(self.data2)        #特殊字节转化
        data = frame_header + frame_addres1 + frame_addres2 + frame_type1 + frame_type2 + data1 + data3 + check_code + frame_end
        self.a.send(data)
        msg1 = self.a.recv(self.size * 2)
        if len(msg1) == 1460:                                           #由于socket的recv接收数据限制，数据量大于1460时，大概率接收1460个字节就阻塞，故增加for循环，使之继续接收
            for j in range(self.size // 1460):
                msg2 = self.a.recv(self.size * 2)
                msg1 += msg2
                if len(msg2) != 1460:
                    break
        msg = self.reverse_byte(msg1)                                   #特殊字节反转
        if file_name in ['current.json','play.lst']:                    #'currentframe.bmp'文件的日志太多,选择不输出
            self.write(f'{self.get_time()} send data({self.i}): ')
            self.write(self.data_16(data.hex()))
            self.write('receive data: ')
            self.write(self.data_16(msg1.hex()))
        if file_name == 'play.lst':
            self.ddd += msg[3:-3].decode('gbk')
            self.ddd = self.ddd.replace('\r', '')
        elif file_name == 'current.json':
            if len(msg[3:-3].hex()) / 2 == self.size:                #接收的数据 = blocksize 继续接收
                self.ddd += msg[3:-3].decode('utf-8')
                d1 = int(('0x' + self.data2.hex()), 16) + self.size  # 文件偏移指针+size并转化
                d2 = hex(d1)[2:].zfill(8)  # zfill——字符串向前补0
                self.data2 = base64.b16decode(d2.upper())
                self.i += 1
                self.download_file(file_name)  # 递归，再次发送接受
            else:
                self.ddd += msg[3:-3].decode('utf-8')
        elif file_name == 'currentframe.bmp':
            if len(msg[3:-3].hex()) / 2 == self.size:
                self.ccc += msg[3:-3]
                d1 = int(('0x' + self.data2.hex()), 16) + self.size     # 文件偏移指针+size并转化
                d2 = hex(d1)[2:].zfill(8)  # zfill——字符串向前补0
                self.data2 = base64.b16decode(d2.upper())
                self.i += 1
                self.download_file(file_name)                           #递归
            else:
                self.ccc += msg[3:-3]


    def message(self,file_name,path):
        self.write('----------------------------------------------------')  # 写入日志
        self.write(f'{self.get_time()} 开始从可变信息标志下载文件{file_name} ... ...')
        self.download_file(file_name)
        if file_name == 'current.json':
            self.write_data(self.ddd, path)                             # 写入文件
        elif file_name == 'play.lst':
            self.write_data(self.ddd, path)
        elif file_name == 'currentframe.bmp':
            with open(path, 'wb') as f:
                f.write(self.ccc)
        self.write(f'{self.get_time()} 从可变信息标志下载文件 {file_name} 成功')
        self.write(f'{self.get_time()} 文件保存在 {path}')


if __name__ == '__main__':
    g = Get_File('10.10.10.188')
    # g.message('current.json','current.json')
    g.message('currentframe.bmp','currentframe.bmp')


