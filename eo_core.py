#!/usr/bin/python3
# coding: utf-8

"""
:A: 对不同页面的爬取需要修改该处的值[1]
:param xxxxxx:按照注释自行设置相应的值
"""

import sys
import os
import time, datetime
import hashlib
import requests
from lxml import html
import smtplib
from email import (header)
from email.mime import (text, multipart)

flag = 0
NowDate = datetime.date.today()+datetime.timedelta(days=+0)
YesDate = datetime.date.today()+datetime.timedelta(days=-1)
msg_title = "机器人风险提示"
msg_head = '<p style="color:#507383">亲爱的主人：</p>'
msg_content = '<p style="font-size:34px;color:#ca1b0f;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">账号被风控，请及时处理！</span></p>'

def MD5(string): # 将爬取的条目转换成MD5方便对信息的比对
    """
    计算字符串md5值
    :param string: 输入字符串
    :return: 字符串md5
    """
    m = hashlib.md5()
    m.update(string.encode())
    return m.hexdigest()

def isEmpty(): #判断文件是否为空
    with open(NowDate.isoformat()+'A' + '.txt', 'r+', encoding="utf-8") as file:
        print(len(file.read()))

def delete():
    try:
        os.remove(YesDate.isoformat()+'A'+'.txt')
        print("A昨天的文件已经删除！")
        return True
    except:
        print("A昨日的文件找不到文件!")
        return False

def compare(string): #比较并判断MD5
    global flag
    with open(NowDate.isoformat()+'A' + '.txt', 'r+', encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if string in line:
                print("ok")
                flag = 1
            else:
                continue
        file.close()

def sender_mail(): #构造邮件并发送邮件
    smtp_Obj = smtplib.SMTP_SSL('smtp.qq.com', 465) #采用pop3/stmp邮箱服务,仅支持qq邮箱[1]
    sender_addrs = 'xxxxxx' #作为服务器的qq邮箱号[1]
    password = "xxxxxx" #该qq邮箱使用pop3/stmp服务的授权码[1]
    smtp_Obj.login(sender_addrs, password)
    receiver_addrs = ['xxxxxx'] #接收邮件的qq邮箱号[1]
    for email_addrs in receiver_addrs:
        try:
            msg = multipart.MIMEMultipart()
            msg['From'] = "InetGeek"
            msg['To'] = email_addrs
            msg['subject'] = header.Header(msg_title, 'utf-8')
            msg.attach(text.MIMEText(msg_content, 'html', 'utf-8'))
            smtp_Obj.sendmail(sender_addrs, email_addrs, msg.as_string())
            print('成功发送给%s' % (email_addrs))
        except Exception as e:
            continue
    smtp_Obj.quit()


# @scheduler.scheduled_job('cron', minute='*/1', id='sleep1')
async def _init_(): #个人自用请去掉异步io(删掉async)
    delete()
    _FLAG_ = 0
    global flag
    print("flag:", flag)
    send_title = "[级网最新通知]\n\n"
    send_content = ""
    _url = 'xxxxxx' #改成eo各年级[通知公告]页面的链接[1]
    response = requests.get(_url)
    response.encoding = "UTF-8"
    selector = html.fromstring(response.text)
    sites = selector.xpath("//*[@id='wp_news_w3']/ul/li")
    if os.path.isfile(NowDate.isoformat()+'A'+'.txt') == False: #当天第一则通知
        print("A不存在,第一次创建任务A")
        with open(NowDate.isoformat()+'A'+'.txt', 'a+', encoding="utf-8") as file:
            for site in sites:
                time = site.xpath('div[@class="fields ex_fields"]/span[@class="Article_PublishDate"]')[0].xpath("string(.)")
                url = site.xpath('div[@class="fields pr_fields"]/span[@class="Article_Title"]/a/@href')[0]
                title = site.xpath('div[@class="fields pr_fields"]/span[@class="Article_Title"]/a/@title')[0]
                if str(time) == str(NowDate):
                    send_content = send_content+time+' '+title+':'+'https://xxxxx.edu.cn'+url+'\n\n'
                    file.write(MD5(title)+'\n')
            file.close()
        with open(NowDate.isoformat()+'A' + '.txt', 'r+', encoding="utf-8") as file:
            if len(file.read()) > 0:
                try: #下面一句替换成你要发送的方式,如采用微信推送则换成push+的发送接口,不要直接用下面一行代码
                    await bot.send_group_msg(group_id=2xxxxx7, message=send_title+send_content + '[CQ:at,qq=all]\n'+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                except: #若发生异常则邮件通知开发者
                    sender_mail()
                    sys.exit()
            else:
                print("A级网今日暂无通知")
            file.close()
    else:
        print("A存在,已经创建过任务")
        with open(NowDate.isoformat()+'A' + '.txt', 'a+', encoding="utf-8") as file:#当天非第一则通知
            for site in sites:
                time = site.xpath('div[@class="fields ex_fields"]/span[@class="Article_PublishDate"]')[0].xpath("string(.)")
                url = site.xpath('div[@class="fields pr_fields"]/span[@class="Article_Title"]/a/@href')[0]
                title = site.xpath('div[@class="fields pr_fields"]/span[@class="Article_Title"]/a/@title')[0]
                if str(time) == str(NowDate):
                    send_content = send_content+time+' '+title+':'+'https://xxxxx.edu.cn'+url+'\n\n'
                    compare(MD5(title))
                    if flag == 1:
                        print("A相同，不写入，不发送，级网暂无新通知,今天有过通知")
                        flag = 0
                    else:
                        flag = 0
                        _FLAG_ = 1
                        file.write(MD5(title) + '\n')
                        print("A不同，写入成功并发送新通知,今天有过通知")
            if _FLAG_ == 1:
                try:#下面一句替换成你要发送的方式,如采用微信推送则换成push+的发送接口,不要直接用下面一行代码
                    await bot.send_group_msg(group_id=2xxxxxx7,message=send_title + send_content + '[CQ:at,qq=all]\n' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                except:
                    sender_mail()
                    sys.exit()
            file.close()
    with open(NowDate.isoformat()+'B' + '.txt', 'r+', encoding="utf-8") as file:
            if len(file.read()) == 0:
                print("A级网今日无暂无通知")
                file.close()
            else:
                file.close()

if __name__ == '__main__':
    _init_()
