#!/usr/bin/python3
# coding: utf-8

import sys
import os, time, datetime
import nonebot
from nonebot import require
import smtplib
from email import (header)
from email.mime import (text, multipart)

with open(r'/home/CCBot/src/plugins/jwc_notice.txt', "r+", encoding="utf-8") as file:
    a = file.read()

send_title = "机器人风险提示"
send_head = '<p style="color:#507383">亲爱的主人：</p>'
send_content = '<p style="font-size:34px;color:#ca1b0f;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">账号被风控，请及时处理！</span></p>'+'<hr><p style="color:#FC5531">教务处通知为:<p>\n\n'+a

def sender_mail():
    smtp_Obj = smtplib.SMTP_SSL('smtp.qq.com',465)
    sender_addrs = 'digran@foxmail.com'
    password = "uavcniivsooqdige"
    smtp_Obj.login(sender_addrs, password)
    receiver_addrs = ['ranshens@foxmail.com']
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

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour = 22,minute = 50)
async def _3():
    with open(r'/home/CCBot/src/plugins/jwc_notice.txt', "r+", encoding="utf-8") as file:
        a = file.read()
        bot = nonebot.get_bots()['2183939725']
        if len(a) > 0:
            try:
                await bot.send_msg(user_id=1348539882, message=a+'\n'+'\n当前时间: '+Nowtime)
                await bot.send_group_msg(group_id=201921077, message=a+'\n [CQ:at,qq=all]'+'\n当前时间: '+Nowtime)
                file.seek(0)
                file.truncate()
            except:
                sender_mail()
                file.seek(0)
                file.truncate()
                sys.exit()
                
