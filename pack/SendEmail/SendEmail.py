import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random


class EmailManage():
    def __init__(self):
        self.smtp_server_qq = 'smtp.qq.com'
        self.mail_user_qq = '2290227486@qq.com'
        self.mail_pass_qq = 'cjkvnaikorekechg'

        self.smtp_server_163 = 'smtp.163.com'
        self.mail_user_163 = '15083837316@163.com'
        self.mail_pass_163 = 'FJMPZJUKWQYMZHBU'

    def GenerateVCode(self):
        code_list = random.sample(range(0, 9), 4)
        code_list = [str(i) for i in code_list]
        Vcode = s=''.join(code_list)
        return Vcode

    def SendVcodeby(self,to_addr,Vcode,SendType):
        if SendType == 'qq':
            mail_user = self.mail_user_qq
            mail_pass = self.mail_pass_qq
            smtp_server = self.smtp_server_qq
        elif SendType == '163':
            mail_user = self.mail_user_163
            mail_pass = self.mail_pass_163
            smtp_server = self.smtp_server_163
        else:
            return 'Verify you SendEmail'
        msg = MIMEText('小黑云验证码为：{}'.format(str(Vcode)), 'plain', 'utf-8')
        # 邮件头信息
        msg['From'] = Header(mail_user)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('小黑云验证码')
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(smtp_server)
        # server = smtplib.SMTP_SSL()
        server.connect(smtp_server, 465)
        # 登录发信邮箱
        server.login(mail_user,mail_pass)
        # 发送邮件
        server.sendmail(mail_user, to_addr, msg.as_string())
        # 关闭服务器
        server.quit()
        return 'ok'
# Em = EmailManage()
# Vcode = Em.GenerateVCode()
# Em.SendMessagebyQq('2290227486@qq.com',Vcode,'163')