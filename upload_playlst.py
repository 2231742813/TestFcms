from Set_log import logger
from set_blocksize import SetBlocksize
from FcmsTool import FcmsTool


class Upload(FcmsTool) :
    def __init__(self, ip='202.11.11.1', port=2929) :
        super().__init__(ip, port)
        # SetBlocksize(ip, port).setblocksize()

    def upload(self, playlist='123') :
        frame_type = b'10'
        document_name = 'play.lst'
        image_datas = playlist.encode('gbk')

        length = len(image_datas)
        step_length = 1024

        number_of_data = int(length // step_length)

        logger.info("frames数量:{0} \n".format(number_of_data))

        for i in range(number_of_data+1) :
            start = i * step_length
            end = start + step_length

            # 获取当前片段的内容
            image_data = image_datas[start :end]

            logger.info("第{}次上载: \n".format(i))
            datas = image_data[step_length * i :step_length * i + step_length :]  # 字节

            offset = (step_length * i).to_bytes(4, byteorder = 'big', signed = True)

            frame_data = document_name.encode('utf-8') + b'\x2B' + offset + image_data
            # 校验码拼接,拼接后为转为hex
            check_code = ((self.frame_addres1 + self.frame_addres2 + frame_type + frame_data).hex())

            # crc检验
            check_code = self.crc16_xmodem(check_code)

            frame_data = self.send_byte(frame_data)

            # 组合帧Data
            data = self.frame_headers + frame_type + frame_data + check_code + self.frame_end
            # 发送数据
            self.a.send(data)
            # 接受返回数据
            msg = self.a.recv(step_length)
            msg = msg.hex()
            msg = msg[7 :8 :]
            if msg == '0' :
                logger.info("设备{} {} 上载播放表成功".format(self.ip,self.port))
                print("设备{} {} 上载播放表成功".format(self.ip,self.port))
                return 1
            else :
                logger.error("设备{} {} 上载播放表 Failed".format(self.ip, self.port))
                print("设备{} {} 上载播放表 Faile".format(self.ip, self.port))
                return 0
#
# # # playlist = '[playlist]\nnwindows=8\nwindows0_x=0\nwindows0_y=0\nwindows0_w=128\nwindows0_h=192\nitem_no = 1             \nitem0 = 300, 1, 0,\\b255000000000\\C010010\\c255255000000\\fk4848红色\\n区域\nwindows1_x=128\nwindows1_y=0\nwindows1_w=128\nwindows1_h=192\nwindows1_item_no = 1       \nwindows1_item0=300, 1, 0,\\b000255000000\\C020020\\fk4848绿色\\n区域\nwindows2_x=256\nwindows2_y=0\nwindows2_w=128\nwindows2_h=192\nwindows2_item_no = 1       \nwindows2_item0=300, 1, 0,\\b000000255000\\C030030\\fk4848蓝色\\n区域\nwindows3_x=384\nwindows3_y=0\nwindows3_w=128\nwindows3_h=192\nwindows3_item_no = 1       \nwindows3_item0=300, 1, 0,\\C000090\\fk4848黄色\\n区域\nwindows4_x=0\nwindows4_y=192\nwindows4_w=128\nwindows4_h=192\nwindows4_item_no = 1       \nwindows4_item0=300, 1, 0,\\c255000000000\\fk4848红色\\n字体\nwindows5_x=128\nwindows5_y=192\nwindows5_w=128\nwindows5_h=192\nwindows5_item_no = 1       \nwindows5_item0=300, 1, 0,\\fk6464楷体\\n64\nwindows6_x=256\nwindows6_y=192\nwindows6_w=128\nwindows6_h=192\nwindows6_item_no = 1       \nwindows6_item0=300, 1, 0,\\fk4848楷体\\n48\nwindows7_x=384\nwindows7_y=192\nwindows7_w=128\nwindows7_h=192\nwindows7_item_no = 1       \nwindows7_item0=300, 1, 0,\\c255000000000红色\\c000255000000绿色\\c000000255000蓝色\\n\\c255255000000黄色\\c255000255000粉色\\c000255255000青色\\n\\c255255255000白色\\c000000000000黑色\\b255255255000'
# playlist = '[playlist] item_no = 1 item0 = 500,1,0,\Pa00\C050050\Pa01'
# if __name__ == "__main__":
#     res = Upload(ip='10.10.10.188', port=2929).upload(playlist='playlist')
#     print(res)