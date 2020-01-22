# -*- coding: utf-8 -*-
# __author__ = 'lusn'
# -*- coding: utf-8 -*-
# __author__ = 'lusn'
import paramiko
import os
def sftp_upload_file(user,password,host,server_path, local_path):
    #单个文件上传、下载
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
    except Exception as e:
        print ("Exception1:",e)

def sftp_download_file(user,password,host,server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path,local_path)
        t.close()
    except Exception as e:
        print ("Exception2:",e)

def sftp_updown_file(updown,user,password,host,server_path, local_path):
    if updown=='up':
        sftp_upload_file(user,password,host,server_path, local_path)
    else:
        sftp_download_file(user,password,host,server_path, local_path)

'''
根据输入参数判断是文件还是目录，进行上传和下载
本地参数local需要与远程参数remote类型一致，文件以文件名结尾，目录以\结尾
上传和下载的本地和远程目录需要存在
异常捕获
'''
def upgrade_sftp_upload_file(user,password,host,server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if os.path.isdir(local_path):#判断本地参数是目录还是文件
            for f in os.listdir(local_path):#遍历本地目录
                sftp.put(os.path.join(local_path+f),os.path.join(server_path+f))#上传目录中的所有文件
        else:
             sftp.put(local_path, server_path)     #上传单个文件
        print("Dir/file upload OK")
        t.close()
    except Exception as e:
        print ("upload Exception:",e)
def upgrade_sftp_download_file(user,password,host,server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if os.path.isdir(local_path):#判断参数是目录还是文件
            for f in sftp.listdir(server_path):#遍历远程目录        1、目录 目录下所有文件遍历download
                sftp.get(os.path.join(server_path+f),os.path.join(local_path+f))#下载目录中所有文件
        else:
            sftp.get(server_path,local_path)#下载单个文件
        print("Dir/file download OK")
        t.close()
    except Exception as e:
        print('download exception:',e)

def upgrade_sftp_updown_file(updown,user,password,host,server_path, local_path):
    if updown=='up':
        upgrade_sftp_upload_file(user,password,host,server_path, local_path)
    else:
        upgrade_sftp_download_file(user,password,host,server_path, local_path)

if __name__ == "__main__":
    #单个文件updown
    sftp_updown_file("up","root","lusainan","192.168.100.118",\
                     "/opt/temp/dir1/3.png",\
                     "D:/auto_test_nancy/coingame/data/picture/3.png")  #up  非up  上传/下载当文件

    # sftp_upload_file("root","lusainan","192.168.100.118",\
    #                  "/opt/temp/dir1/1.png",\
    #                  "D:/auto_test_nancy/coingame/data/picture/1.png") #上传文件 单个文件 D:\\web_http\\112255\\11.png

    #升级版本1：可以判断是文件还是目录，来上传单个文件或者整个目录
    # upgrade_sftp_updown_file("u1p","root","lusainan","192.168.100.118",\
    #                  "/opt/temp/dir1/4.png",\
    #                  "D:/auto_test_nancy/coingame/data/picture/4.png")# 单个文件----1
    #
    # upgrade_sftp_updown_file("u1p","root","lusainan","192.168.100.118",\
    #                  "/opt/temp/dir1/",\
    #                  "D:/auto_test_nancy/coingame/data/picture/")# 遍历文件，整个目录 ----2