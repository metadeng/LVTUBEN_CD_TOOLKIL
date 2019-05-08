#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:denghuabing@cecgw.cn
# date:2017/11/16
# version:1.0

import smtplib
import glob
import re
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage


def send_mail(sender_mail, subject, mail_content, to_list, sender_name='',
              sender_passwd='', cc_list=[], image_path=None, attach_path=None):
    """
    send mail
    :param sender_mail:     发件人的邮箱
    :param subject:         邮件标题
    :param mail_content:    邮件内容(html形式）
    :param to_list:         收件人列表
    :param sender_name:     发件人的姓名
    :param sender_passwd:   发件人的邮箱密码
    :param cc_list:         抄送人列表，默认为空
    :param image_path:      发送图片的路径，如果邮件内容中包含有图片，将所有的图片放在image_path路径下，发送时会从该路径读取所有的图片
    :param attach_path:     附件的路径，该路径下的所有东西都会当做附件发送
    :return:
    """
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    if sender_name:
        msg['From'] = '"%s" <%s>' % (sender_name, sender_mail)
    else:
        msg['From'] = sender_mail

    if to_list:
        for to in to_list:
            msg['To'] = to.strip()
    if cc_list:
        for cc in cc_list:
            msg['Cc'] = cc.strip()
    address_list = set(to_list) | set(cc_list)

    content_part = MIMEMultipart('related')
    html_part = MIMEBase('text', 'html', charset="us-ascii")
    html_part.set_payload(mail_content)
    encoders.encode_base64(html_part)
    html_part["Content-Disposition"] = 'filename="%s.html"' % \
                                       subject.replace(' ', '_')
    content_part.attach(html_part)
    if image_path:
        image_set = set()
        for image_str in re.findall(
                '<\s*img\s+src\s*=\s*\"?\s*cid\s*:\s*[^<>\"]+\s*\"?\s*>',
                mail_content):
            m = re.search(
                '<\s*img\s+src\s*=\s*\"?\s*cid\s*:\s*([^<>\"]+)\s*\"?\s*>',
                image_str)
            if m:
                image_set.add(m.group(1))

        for image_file in list(image_set):
            fo = open(image_path + os.sep + image_file)
            image_part = MIMEImage(fo.read())
            fo.close()
            image_part.add_header('Content-ID', '<%s>' % image_file)
            image_part["Content-Disposition"] = 'filename="%s"' % image_file
            content_part.attach(image_part)
    msg.attach(content_part)

    if attach_path:
        for attach_file in glob.glob(attach_path + os.sep + '*'):
            attach = MIMEBase('application', 'octet-stream')
            fo = open(attach_file, 'rb')
            attach.set_payload(fo.read())
            fo.close()
            encoders.encode_base64(attach)
            attach["Content-Disposition"] = 'attachment; filename="%s"' % \
                                            os.path.split(attach_file)[1]
            msg.attach(attach)

    try:
        server = smtplib.SMTP('smtp.cecgw.cn')
    except Exception as e:
        print("Error occur while connect to mail server:\n%s" % e)
        sys.exit(1)
    if sender_passwd:
        try:
            server.login(sender_mail, sender_passwd)
        except smtplib.SMTPAuthenticationError:
            print("Login mail server failed.")
            server.quit()
            sys.exit(1)
    server.sendmail(msg['From'], list(address_list), msg.as_string())
    server.quit()
