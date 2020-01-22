#smtplib模块主要负责发送邮件，email模块主要负责构造邮件。
#smtplib模块主要负责发送邮件：是一个发送邮件的动作，连接邮箱服务器，登录邮箱，发送邮件（有发件人，收信人，邮件内容）。
#email模块主要负责构造邮件：指的是邮箱页面显示的一些构造，如发件人，收件人，主题，正文，附件等
import smtplib
import unittest
import os
import time
import HTMLTestRunner
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText           #正文
from email.mime.image import MIMEImage
from email.header import Header                #标题
#==============发送图片成功！！！============#

smtpserver = 'smtp.163.com'
user = 'lusainan13579@163.com'
password = '150061803670513'
sender = 'lusainan13579@163.com'
receiver = 'lusainan13579@163.com'


msgRoot = MIMEMultipart('related')
subject = 'Python 自动化测试报告'
msgRoot['Subject'] = subject

##content =  MIMEText('<html><h1>内容如下：</h1></html>','html','utf-8')
##msgRoot.attach(content)

content = MIMEText('<html><h1>内容如下：</h1></html><html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
msgRoot.attach(content)

fp = open('D:\\explore_dfw\\data\\img\\xiaohuangren.png', 'rb')
img_data = MIMEImage(fp.read())
fp.close()

img_data.add_header('Content-ID', 'imageid')
msgRoot.attach(img_data)


msgRoot['from'] = sender
msgRoot['to'] = receiver



try:
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()
    print ("邮件发送成功")

except smtplib.SMTPException as e:  
    print("Error, 发送失败")
    



