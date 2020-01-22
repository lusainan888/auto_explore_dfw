# -*- coding: utf-8 -*-
# __author__ = 'lusn'
import paramiko
import runtest_all
from config import globalparam
report_path = globalparam.get_report_path()

def sftp_upload_file(user,password,host,server_path, local_path):
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


if __name__ == "__main__":
    # report_path="D:/explore_dfw/data/report/"
    localfile=runtest_all.new_file(report_path)
    filename=localfile.split('/')[-1]
    servicefile="/opt/report/"+filename
    sftp_updown_file('up',"root","lusainan","192.168.100.156",\
                     servicefile,\
                     localfile)
