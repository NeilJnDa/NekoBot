# -*- coding: UTF-8 -*-
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time as tm
import numpy
from enum import Enum
from ruamel import yaml


# emun
class Status(Enum):
    filled = '今日已经手动填报，自动填报未进行'
    unfilled = '未填报'
    error = '自动填报出现错误'
    done = '自动填报已完成'
    unknown = '状态未知'


def get_yaml(address):
    print("获取yaml用户数据...")
    file = open(address, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    data = yaml.load(file_data, Loader=yaml.Loader)
    print("获取成功")
    print(data)
    return data


def generate_yaml(address, data):
    print(data)
    file = open(address, 'w', encoding='utf-8')
    yaml.dump(data, file, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    file.close()


def send_email_auto(info):
    email_conf = get_yaml('email.yml')
    if not email_conf['enable']:
        print('邮件设置：任务完成后不发送邮件')
        return
    send_email_by_qq(email_conf, info)


def send_emails_to_all_manual(accounts):
    email_conf = get_yaml('email.yml')
    for each in accounts:
        if each['enable']:
            send_email_by_qq(email_conf, each)


def send_email_by_qq(email, info):
    time = tm.strftime("%m-%d %H.%M", tm.localtime(tm.time()))
    sender_mail = email['sender_mail']
    sender_pass = email['sender_pass']
    # 收件人
    to = info['email']
    # 设置总的邮件体对象，对象类型为mixed
    msg_root = MIMEMultipart('mixed')
    # 邮件添加的头尾信息等
    msg_root['From'] = email['from']
    msg_root['To'] = to
    # 邮件的主题，显示在接收邮件的预览页面
    subject = email['subject']
    msg_root['subject'] = Header(subject, 'utf-8')

    # 构造文本内容
    # content = """
    # <html>
    #     <body>
    # <h1>中午好~</h1>
    # <p>今日填报结果：</p>
    # <p>""" + info['id'] + ': ' + info['status'].value + """</p>
    # <p>今天我自己的是手动填的，因为要写不返校申请</p>
    # <p>如果自动填报失败，那可能需要自己去开系统填一下~ 管理员可能在睡觉zzzzZZZZ</p>
    #     </body>
    # </html>
    # """
    # <p>若对此邮件内容有疑问，请联系那个问你要邮箱的人 OuO </p>
    # <p>""" + time + """</p>
    content = '</body></html>'
    content += email['content1'] + '<p>今日填报结果 :'
    try:
        status = info['status'].value
    except:
        status = '无需显示'
    finally:
        content += info['id'] + '——' + status + '</p>' + email['content2']
        content += '<p>' + time + '</p>' + '</body></html>'
        msg = MIMEText(content, _subtype='html', _charset='utf-8')  # 这里看email模块的说明，这里构造内容
        msg_root.attach(msg)

    # # 构造超文本
    # url = "https://blog.csdn.net/chinesepython"
    # html_info = """
    # <p>点击以下链接，你会去向一个更大的世界</p>
    # <p><a href="%s">click me</a></p>
    # <p>i am very galsses for you</p>
    # """% url
    # html_sub = MIMEText(html_info, 'html', 'utf-8')
    # # 如果不加下边这行代码的话，上边的文本是不会正常显示的，会把超文本的内容当做文本显示
    # html_sub["Content-Disposition"] = 'attachment; filename="csdn.html"'
    # # 把构造的内容写到邮件体中
    # msg_root.attach(html_sub)

    # 构造图片
    # image_file = open(r'F:\Selenium\Log\04-11 20.50\213162797.png', 'rb').read()
    # image = MIMEImage(image_file)
    # image.add_header('Content-ID', '<image1>')
    # # 如果不加下边这行代码的话，会在收件方方面显示乱码的bin文件，下载之后也不能正常打开
    # image["Content-Disposition"] = 'attachment; filename="red_people.png"'
    # msg_root.attach(image)

    # # 构造附件
    # txt_file = open(r'D:\python_files\files\hello_world.txt', 'rb').read()
    # txt = MIMEText(txt_file, 'base64', 'utf-8')
    # txt["Content-Type"] = 'application/octet-stream'
    # #以下代码可以重命名附件为hello_world.txt
    # txt.add_header('Content-Disposition', 'attachment', filename='hello_world.txt')
    # msg_root.attach(txt)

    try:
        sftp_obj = smtplib.SMTP('smtp.qq.com', 25)
        sftp_obj.login(sender_mail, sender_pass)
        sftp_obj.sendmail(sender_mail, to, msg_root.as_string())
        sftp_obj.quit()
        print('sendemail to ' + info['name'] + ' ' + to + ' successful!')

    except Exception as e:
        print('sendemail failed next is the reason')
        print(e)


if __name__ == '__main__':
    # 可以是一个列表，支持多个邮件地址同时发送，测试改成自己的邮箱地址
    picture_time = time.strftime("%m-%d %H.%M", time.localtime(time.time()))
    log = {'id': '213162797', 'password': '14789ldj', 'email': '15651991790@163.com', 'status': Status.unknown}
    send_email_by_qq(log, picture_time)

