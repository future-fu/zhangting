# coding:utf-8
import smtplib
import threading
from email.mime.text import MIMEText
from email.header import Header
import os,threading,time
from yeji import file_to_str


class Mail:
    def __init__(self):
        # 第三方 SMTP 服务

        self.mail_host = "smtp.qq.com"  # 设置服务器:这个是qq邮箱服务器，直接复制就可以
        self.mail_pass = "uzalcdtwrbfybjjg"  # 刚才我们获取的授权码
        self.sender = '344600595@qq.com'  # 你的邮箱地址
        self.receivers = ['344600595@qq.com']  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个

    def send(self):
        str1 = ''
        with open('C://work/pythoncoding/zhangting/data/res.csv', mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                str1 += line
        print(str1)
        content = str(str1)
        print(content)
        message = MIMEText(content, 'plain', 'utf-8')

        message['From'] = Header("业绩", 'utf-8')
        message['To'] = Header("qq邮箱", 'utf-8')

        subject = '业绩预测'  # 发送的主题，可自由填写
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()

            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败')


def dinshi():
    curTime = time.strftime("%Y-%M-%D", time.localtime())  # 记录当前时间
    execF = False
    ncount = 0

    def execTask():
        # 具体任务执行内容
        mail = Mail()
        mail.send()
        print("execTask executed!")

    def timerTask():
        global execF
        global curTime
        global ncount
        if execF is False:
            execTask()  # 判断任务是否执行过，没有执行就执行
            execF = True
        else:  # 任务执行过，判断时间是否新的一天。如果是就执行任务
            desTime = time.strftime("%Y-%M-%D", time.localtime())
            if desTime > curTime:
                execF = False  # 任务执行执行置值为
                curTime = desTime
        ncount = ncount + 1
        timer = threading.Timer(5, timerTask)
        timer.start()
        print("定时器执行%d次" % (ncount))


if __name__ == '__main__':
    dinshi()
    mail = Mail()
    mail.send()
    #
    #
    # def fun_timer():
    #     print('Hello Timer!')
    #     mail.send()
    #     global timer
    #     timer = threading.Timer(30, fun_timer)
    #     timer.start()
    #
    #
    # timer = threading.Timer(1, fun_timer)
    # timer.start()
