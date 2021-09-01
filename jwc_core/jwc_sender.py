#!/usr/bin/python3
# coding: utf-8

import sys
import os, time, datetime
import smtplib
from email import (header)
from email.mime import (text, multipart)

with open(r'/home/jwc_notice.txt', "r+", encoding="utf-8") as file: #自行更改路径
    a = file.read()

send_title = "机器人风险提示"
send_head = '<p style="color:#507383">亲爱的主人：</p>'
send_content = '<p style="font-size:34px;color:#ca1b0f;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">账号被风控，请及时处理！</span></p>'+'<hr><p style="color:#FC5531">教务处通知为:<p>\n\n'+a

def sender_mail():
    smtp_Obj = smtplib.SMTP_SSL('smtp.qq.com',465)
    sender_addrs = 'xxxxxx'
    password = "xxxxxx"
    smtp_Obj.login(sender_addrs, password)
    receiver_addrs = ['xxxxxx']
    for email_addrs in receiver_addrs:
        try:
            msg = multipart.MIMEMultipart()
            msg['From'] = "InetGeek"
            msg['To'] = email_addrs
            msg['subject'] = header.Header(send_title, 'utf-8')
            msg.attach(text.MIMEText(send_content, 'html', 'utf-8'))
            smtp_Obj.sendmail(sender_addrs, email_addrs, msg.as_string())
            print('成功发送给%s' % ( email_addrs))
        except Exception as e:
            continue
    smtp_Obj.quit()

Nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# @scheduler.scheduled_job('cron', hour = 22,minute = 50)
async def _init_():#个人自用请去掉异步io(删掉async)
    with open(r'/home/jwc_notice.txt', "r+", encoding="utf-8") as file:
        a = file.read()
        if len(a) > 0:
            try:#下面两句句替换成你要发送的方式,如采用微信推送则换成push+的发送接口,不要直接用下面两行代码
                await bot.send_msg(user_id=1xxxxxxx2, message=a+'\n'+'\n当前时间: '+Nowtime)
                await bot.send_group_msg(group_id=2xxxxxxxx7, message=a+'\n [CQ:at,qq=all]'+'\n当前时间: '+Nowtime)
                file.seek(0)
                file.truncate()
            except:
                sender_mail()
                file.seek(0)
                file.truncate()
                sys.exit()
if __name__ == '__main__':
    _init_()
