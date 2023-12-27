# def test_upload_playlists(self):
#             with open('./data/{}'.format(case_name), encoding='utf-8') as f:
#                 datas = csv.reader(f)
#                 for line in datas:
#                     playlist_id, camera_or_video, wait_time, titles, playlists = line
#                     logger.info("播放表信息 playlist_id, camera_or_video, wait_time, titles, playlists")
#                     logger.info(line)
#
#                     affirm_playlists = playlists
#                     now = time.localtime()
#                     now_time = time.strftime("[%m-%d %H:%M:%S]", now)
#                     self.show_text.AppendText(
#                         "----------------------------------------------------------------------------------------------------------------------------------\n")
#                     # upload_count += 1
#                     self.show_text.AppendText("{} 上载播放表\n".format(now_time))
#                     self.show_text.AppendText("{0} 播放表格式：\n{1}\n".format(now_time, playlists))
#                     logger.info("开始上载播放表")
#                     logger.info("播放表格式：\n{}".format(playlists))
#                     # 连接设备
#                     socket.setdefaulttimeout(2)
#                     a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                     a.connect(tuple((host, port)))
#                     # 帧头
#                     frame_header = b'\x02'
#                     # 地址
#                     frame_addres1 = b'0'
#                     frame_addres2 = b'0'
#                     # 帧类型
#                     frame_type1 = b'1'
#                     frame_type2 = b'0'
#                     # 帧数据,帧数据由三部分组成，文件名（data），分隔符（data1），文件指针偏移（data3），一段文件内容（data4）
#                     data = 'play.lst'.encode('gbk')
#                     s = data.hex()
#                     check_code_data = data.hex()
#                     data9 = base64.b16decode(s.upper())
#                     data1 = b'\x2B'
#                     check_code_data1 = data1.hex()
#                     data6 = '\0\0\0\0'.encode('gbk')
#                     data7 = playlists.encode('gbk')
#                     data2 = data6 + data7
#                     s2 = data2.hex()
#                     check_code_data2 = data2.hex()
#                     data2 = base64.b16decode(s2.upper())
#                     # 校验码拼接,拼接后为字符串
#                     check_code = (frame_addres1 + frame_addres2 + frame_type1 + frame_type2).hex() \
#                                  + check_code_data + check_code_data1 + check_code_data2
#                     # crc检验
#                     check_code = crc16_xmodem(check_code)
#                     # 转为字节，格式为'\x**\x**'
#                     check_code = base64.b16decode(check_code.upper())
#                     # 帧尾
#                     frame_end = b'\03'
#                     # 组合帧Data
#                     data = frame_header + frame_addres1 + frame_addres2 + frame_type1 + frame_type2 + data9 + data1 + data2 + check_code + frame_end
#                     logger.info("发送数据: {}".format(data.hex()))
#                     # 发送数据
#                     a.send(data)
#                     # 接受返回数据
#                     msg = a.recv(1024)
#                     # 断开连接
#                     a.close()
#                     logger.info("接受数据: {}".format(msg.hex()))
#                     now = time.localtime()
#                     now_time = time.strftime("[%m-%d %H:%M:%S]", now)
#                     self.show_text.AppendText(
#                         "------等待{}s\n".format(interval_time / 2))
#                     logger.info("-----------------------------------等待 {}s ")
#                     time.sleep(interval_time / 2)
#                     now = time.localtime()
#
#                     if whether_camera == 1:
#                         # 调用相机拍照
#                         picture_name = Camera_OR_Video(camera_or_video=int(camera_or_video),
#                                                        wait_time=int(wait_time), titles=titles,
#                                                        descriptions=playlists)
#                         self.show_text.AppendText(f"图片名称：{picture_name}\n")
#                         self.show_text.write('拍照功能启用\n')
#                         logger.info(f"图片名称：{picture_name}")
#                     elif whether_camera == 0:
#                         logger.info("拍照功能关闭")
#                         self.show_text.write('拍照功能关闭\n')
#                     else:
#                         logger.error('whether_camera参数错误')
#
#                     # version = self.get_version()
#                     # print(version)
#                     # version = int(version[0 :1 :])
#                     # print(version)
#                     # logger.info("大版本号： %s", version)
#
#                     now = time.localtime()
#                     now_time = time.strftime("[%m-%d %H:%M:%S]", now)
#
#                     self.show_text.AppendText(
#                         "{0} 开始取currentframe.bmp\n".format(now_time))
#
#                     version = Fcms_version
#                     logger.info("Fcms_version {}".format(version))
#                     if save_or_contrast_bmp == 0:
#                         if version == 2:
#                             self.down_bmp(save_bmp_url + str(playlist_id) + '.bmp')
#                             time.sleep(interval_time / 2)
#                         elif version == 3:
#                             self.down_bmp(save_bmp_url + str(playlist_id) + '.bmp')
#                             time.sleep(interval_time / 2)
#                         else:
#                             logger.error('Fcms_version获取异常')
#                     elif save_or_contrast_bmp == 1:
#                         if version == 2:
#                             self.down_bmp('./picture/test/{}.bmp'.format(playlist_id))
#                             time.sleep(interval_time / 4)
#                             # 2版本对比图片
#                             contrast_result = CompareImage().compare_image(
#                                 './picture/test/{}.bmp'.format(playlist_id),
#                                 './picture/2/{}.bmp'.format(playlist_id), playlist_id)
#                             if contrast_result == 1:
#                                 self.show_text.write("2.X版本图片对比                成功\n")
#                                 logger.info('2.X版本图片对比成功')
#                             elif contrast_result == 0:
#                                 self.show_text.write("2.X版本图片对比        失败\n")
#                                 logger.warn('2.X版本图片对比失败')
#                                 Wenhook_send_picuter_result(playlist_id, playlists)
#                             else:
#                                 self.show_text.write("2.X版本图片对比出现异常\n")
#                                 logger.warn('2.X版本图片对比出现异常')
#                             time.sleep(interval_time / 4)
#                         elif version == 3:
#                             self.down_bmp('./picture/test/{}.bmp'.format(playlist_id))
#                             time.sleep(interval_time / 4)
#                             # 3版本对比图片
#                             contrast_result = CompareImage().compare_image(
#                                 './picture/test/{}.bmp'.format(playlist_id),
#                                 './picture/3/{}.bmp'.format(playlist_id), playlist_id)
#
#                             if contrast_result == 1:
#                                 self.show_text.write("3.X版本图片对比                成功\n")
#                                 logger.info('3.X版本图片对比成功')
#                             elif contrast_result == 0:
#                                 self.show_text.write("3.X版本图片对比        失败\n")
#                                 logger.warn('3.X版本图片对比失败')
#                                 Wenhook_send_picuter_result(playlist_id, playlists)
#                             else:
#                                 self.show_text.write("3.X版本图片对比出现异常\n")
#                                 logger.warn('3.X版本图片对比出现异常')
#                             time.sleep(interval_time / 4)
#                         else:
#                             logger.error('文件对比出现异常异常')
#                     else:
#                         logger.error("save_or_contrast_bmp参数错误")
#
#
#                     if whether_str_affirm == 1:
#                         now = time.localtime()
#                         now_time = time.strftime("[%m-%d %H:%M:%S]", now)
#
#                         affirm_msg = self.test_get_device_show_content(event=1)
#                         affirm_playlists2 = affirm_playlists.split(',', 3)
#                         affirm_playlists2 = affirm_playlists2[len(affirm_playlists2) - 1]
#                         self.show_text.AppendText("{0} 上载的字符串 {1}\n".format(now_time, affirm_playlists2))
#                         self.show_text.AppendText("{0} 当前显示字符串 {1}\n".format(now_time, affirm_msg))
#                         affirm_playlists1 = affirm_playlists.split(',', 3)
#                         affirm_playlists1 = affirm_playlists1[len(affirm_playlists1) - 1]
#                         if affirm_playlists1 == affirm_msg:
#                             self.show_text.AppendText("{} 断言           成功\n\n".format(now_time))
#                         else:
#                             self.show_text.AppendText("{} 断言      失败\n\n".format(now_time))
#                         time.sleep(1)
#                     elif whether_str_affirm == 0:
#                         self.show_text.AppendText('字符串断言关闭\n')
#                         logger.info('字符串断言关闭')
#                     else:
#                         logger.error('whether_str_affirm参数错误')
#
#                     if not self.running:
#                         break
#
#             x -= 1
#             if not self.running:
#                 break
#             else:
#                 continue