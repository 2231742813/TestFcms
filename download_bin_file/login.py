import requests
import re

headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
}
url_login = "https://git.sansi.net:6101/users/sign_in"
url_login_action = "https://git.sansi.net:6101/"

url1 = 'https://git.sansi.net:6101/common_display/Embedded_Software/x90/xstudiopro/xstudiopro-publish/-/pipelines'

# 创建session对象
session = requests.session()
# 使用session发送请求，对应的响应中的cookie会自动保存到sesison对象中
response = session.get(url = url_login, headers = headers)
print(response.status_code)
print("cookie:", response.cookies)
# 获取响应内容
content = response.content.decode("utf-8")
# print(content)
# 获取token
authenticity_token = re.findall(r'name="authenticity_token" value="(.*?)"', content)[0]
# print(authenticity_token)
# # 准备参数
data = {
    "authenticity_token" : authenticity_token,
    "login" : 'chenpeng@sansi.com',
    "password" : 'cp9801131',
    'remember_me' : '0'
}
# 使用session发送请求，上次存储的当前网站的cookie会自动发送过去
response2 = session.get(url = url_login, headers = headers, data = data)
# # 获取响应内容
# # print(response2.content.decode("utf-8"))
print(response2.status_code)
print(response2.text)

# response3 = session.get(url = url1, headers = headers)
# print(response3.text)
