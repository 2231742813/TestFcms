from Set_log import logger
from set_blocksize import SetBlocksize
from FcmsTool import FcmsTool


class Upload(FcmsTool) :
    def __init__(self, ip='202.11.11.1', port=2929) :
        super().__init__(ip, port)
        SetBlocksize(ip, port).setblocksize()

    def upload(self, document_url='./play.lst', document_name='play.lst') :
        frame_type = b'10'

        with open(r'{}'.format(document_url), 'r',encoding='gbk') as f :
            image_datas = f.read().encode('gbk')


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
                logger.info("发送数据成功 \n")
            else :
                logger.info("发送数据失败\n")

if __name__ == "__main__":
    Upload(ip='192.168.210.88', port=2929).upload(document_url='./play.lst', document_name='play.lst')