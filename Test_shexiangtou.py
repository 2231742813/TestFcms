# -*- coding: utf-8 -*-
# import requests
# from io import BytesIO
# from PIL import Image
#
# # 用户名和密码
# username = 'zf'
# password = 'Sansi1280'
#
# # 网页URL
# url = 'http://172.16.200.23/doc/page/preview.asp'
#
# # 创建一个会话对象
# session = requests.Session()
#
# # 发送带有用户名和密码的POST请求
# response = session.post(url, data={'username': username, 'password': password})
#
# # 检查响应状态码
# if response.status_code == 200:
#     # 打印网页内容
#     print(response.text)
#
#
#     # 将网页内容转换为图像
#     image = Image.open(BytesIO(response.content))
#
#     # 保存图像
#     image.save('webpage.png')
# else:
#     print('Failed to open the webpage.')
#
# # 关闭会话
# session.close()

a = 0x8A
print(a)
# print(a.decode('utf-8'))
# print(type(a))