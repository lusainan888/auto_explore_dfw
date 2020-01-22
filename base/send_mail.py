# -*- coding: utf-8 -*-
# __author__ = 'lusn'
from base.log import Log
import runtest_all
from email.utils import formataddr
from decimal import Decimal
import paramiko
import os,sys
import time
from config import globalparam
import smtplib
from email.mime.text import MIMEText  #正文
from email.header import Header   #标题
from email.mime.image import MIMEImage  #图片
from email.mime.multipart import MIMEMultipart #MIMEMulipart模块构造带附件
import datetime
from config.globalparam import get_send_emails,get_send_pwd,get_receiver_emails,get_acc_emails
logger = Log()

report_path = globalparam.get_report_path()
sender=get_send_emails()
login_pwd=get_send_pwd()
receivers=get_receiver_emails()
acc=get_acc_emails()
report_path=runtest_all.new_file(report_path)
filename=report_path.split('/')[-1]

img_path = globalparam.get_img_path()
img_path=runtest_all.new_file(img_path)
imgname=img_path.split('/')[-1]

# receivers=['lusainan@dfgroup.pro','lusainan13579@163.com']
# acc=['1204038070@qq.com','1060461845@qq.com']

def send_email(isimag='false',isfile='false',sender=sender,login_pwd=login_pwd,
               # receivers=['lusainan13579@163.com']
               receivers=receivers
               ,subject='Python SMTP 邮件测试',
               msg='Dear all:'):

    """发送邮件"""
    # message = MIMEText(msg, 'plain', 'utf-8')
    # message['From'] = sender   # 发送者
    # message['to'] = ','.join(receivers)   # 收件人，必须是一个字符串
    # message['Cc'] = ','.join(acc)
    # message['Subject'] = Header(subject, 'utf-8')

    message = MIMEMultipart('related')   #设置邮件为多文本格式

    ftppath=globalparam.get_sftp()
    clink=ftppath+filename
    msg="<html><h1>%s</h1></html><p><a href=%s>%s</a></p>" %(msg,clink,clink)


    if isimag==True:
        fp = open(img_path, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', 'image1')
        message.attach(msgImage)
        msg2='<html><h1>图片如下：</h1></html><html><body><img src="cid:image1" alt="image1"></body></html>'
        msg=msg+msg2

    content = MIMEText(msg,'html','utf-8')
    message.attach(content)


    # message['From'] = sender   # 发送者
    message['From'] = formataddr(["陆赛男", sender])
    message['to'] = ','.join(receivers)   # 收件人，必须是一个字符串
    message['Cc'] = ','.join(acc)
    message['Subject'] = Header(subject, 'utf-8')

    #构造附件
    if isfile==True:
        sendfile1=open(report_path,'rb').read()
        att1 = MIMEText(sendfile1, 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename=%s'%(filename)
        message.attach(att1)


        sendimage1=open(img_path,'rb').read()#'D:\\explore_dfw\\data\\img\\xiaohuangren.png'
        att2 = MIMEText(sendimage1, 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename=%s'%(imgname)
        message.attach(att2)

        # #将图片显示在正文 html嵌入
        # content = MIMEText('<html><h1>图片如下：</h1></html><html><body><img src="cid:image1" alt="image1"></body></html>','html','utf-8')
        # fp = open(img_path, 'rb')
        # print("1:",img_path)
        # msgImage = MIMEImage(fp.read())
        # msgImage.add_header('Content-ID', 'image1')  #设置图片ID
        # msgImage.add_header('Content-Disposition','attachment',filename='image2.png') #为附件添加一个标题
        # message.attach(msgImage)





    try:
        smtpObj = smtplib.SMTP_SSL('smtp.163.com') #SMTP服务器
        smtpObj.login(sender,login_pwd)  #不是登录邮箱密码，而是授权码
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        logger.info ("邮件发送成功")
    except smtplib.SMTPException:
        logger.info ("Error: 无法发送邮件")


if __name__ == '__main__':
    #多人收件、带附件、带link、正文插入图片等
    # send_email()  #纯文本  OK
    # send_email(True,'false')  #插入图片 OK
    # send_email('false',True)  #附件 OK
    send_email(True,True)  #全部发送 OK
    pass

