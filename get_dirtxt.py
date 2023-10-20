from FcmsTool import FcmsTool


class Get(FcmsTool) :
    def __init__(self, ip='202.11.11.1', port=2929, outtime=10) :
        super().__init__(ip, port, outtime = 2)

    def get_time(self) :
        frame_type1 = b'1'
        frame_type2 = b'4'
        name = '../../log/'.encode('gbk')
        check_code = self.crc16_xmodem(
            (self.frame_addres1 + self.frame_addres2 + frame_type1 + frame_type2 + name).hex())
        self.a.send(self.frame_headers + frame_type1 + frame_type2 + name+ check_code  + self.frame_end)
        res = self.a.recv(2048)
        print(res.hex())


Get().get_time()
