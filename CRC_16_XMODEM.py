# # coding=utf-8
# from binascii import unhexlify
# from crcmod import mkCrcFun
#
#
# def crc16_xmodem(data):
#     data = str(data)
#     data = str(data)
#     crc16 = mkCrcFun(0x11021, rev = False, initCrc = 0x0000, xorOut = 0x0000)
#     check_code = get_crc_value(data, crc16)  # 进行16进制CRC校验
#     check_code = check_code.zfill(4)  # 不足4位补0
#     return check_code
#
#
# # common func
# def get_crc_value(s, crc16):
#     data = s.replace(' ', '')
#     crc_out = hex(crc16(unhexlify(data))).upper()
#     str_list = list(crc_out)
#     if len(str_list) == 5:
#         str_list.insert(2, '0')  # 位数不足补0
#     crc_data = ''.join(str_list[2:])
#     return (crc_data[:2] + crc_data[2:]).lower()
