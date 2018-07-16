import base64
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def smtp_sendmail(mail_user, mail_pass, to_users_list, subject, mail_content):
    """SMTP 邮件发送模块

    :param mail_host:   设置服务器
    :param mail_user:   用户名
    :param mail_pass:   口令
    :param to_users_list:   接收邮件者，可设置为你的QQ邮箱或者其他邮箱，可传入一个邮箱list
    :param name_sender:   设置发件人名称
    :param name_receiver:   设置收件人名称
    :param subject:   设置邮件主题
    :param mail_content:   设置邮件内容
    :return:   无
    """

    # # 第三方 SMTP 服务 （默认配置信息设置区）
    mail_host = "smtp.sina.com"  # 设置服务器
    mail_user = base64.b64decode(mail_user).decode()  # 用户名
    mail_pass = base64.b64decode(mail_pass).decode()  # 口令
    receivers = [base64.b64decode(i).decode() for i in to_users_list]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱，可传入一个邮箱list

    name_sender = "Python_Message"  # 设置发件人名称
    name_receiver = "管理员"  # 设置收件人名称

    # 考虑到编码的原因，这里统一将name属性值改成utf-8，地址的话一定是统一的邮箱地址结构，所以不考虑
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    # 功能区
    message = MIMEText(mail_content, 'html', 'utf-8')
    message['From'] = _format_addr('%s <%s>' % (name_sender, mail_user))
    # message['From'] = formataddr((Header('测试', 'utf-8').encode(),mail_user))
    message['To'] = _format_addr('%s <%s>' % (name_receiver, receivers))
    message['Subject'] = Header(subject, 'utf-8')

    # print(message)

    # 发送区
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 25 为 SMTP 端口号
        # smtpObj.set_debuglevel(1)  # 调试显示邮件发送交互信息
        # smtpObj.starttls()
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")

    except Exception as err:
        print("发送失败！\n原因是：" + str(err))


if __name__ == '__main__':
    smtp_sendmail('nihao', '111')
