import smtplib
import ssl
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from read_yaml import Read_Phone_Camera_Config

# 发送邮件

# 读取yaml配置文件
data = Read_Phone_Camera_Config()
emil_address = data['EMAIL_ADDRESS']
emil_password = data['EMAIL_PASSWORD']
sender = data['SENDER']
receiver = data['RECEIVER']
target_folder = data['target_folder']


def Send_Email(picture_name):
    # 邮箱地址
    EMAIL_ADDRESS = emil_address
    # SMTP的授权码(QQ邮箱设置里）
    EMAIL_PASSWORD = emil_password
    """
    在smtplib中，如果您将context设置为None，这意味着您的SMTP连接将不会使用SSL/TLS加密，即使目标SMTP服务器支持它。这可能会导致您发送的邮件的安全性受到威胁，因为它们可能会在网络传输过程中被拦截或篡改。
    如果您想确保SMTP连接的安全性，我建议您将context参数设置为一个有效的SSLContext对象，以便启用SSL/TLS加密。您也可以考虑使用其他方法（如STARTTLS命令）来启用SMTP连接的加密。
    """
    context = ssl.create_default_context()
    # 邮件的标题
    subject = '手机拍摄图片'
    # 读取图片数据并编码为 base64，以便在 HTML 中嵌入
    with open(target_folder + picture_name, 'rb') as f:
        image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
    # 构造 HTML，其中使用嵌入式数据 URI 将图像添加到HTML中
    html = """
    <html>
        <body>
            <h2>{}</h2>
            <p>图片见下</p>
            <img src='data:image/png;base64,{}'>
        </body>
    </html>
    """.format(subject, encoded_image)

    # 创建 MIMEMultipart 对象并设置邮件内容
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # 添加 HTML 和图像作为替代内容
    msg.attach(MIMEText(html, 'html'))
    msg_img = MIMEImage(image_data, name=os.path.basename(picture_name))
    msg.attach(msg_img)

    # 创建 SMTP 客户端对象并发送邮件
    with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.sendmail(sender, receiver, msg.as_string())

