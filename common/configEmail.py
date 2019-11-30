import os
import smtplib

from common import readConfig
import getpathInfo
from common.Log import Logger
from email.mime.text import MIMEText
from email.header import Header

read_conf = readConfig.ReadConfig()
mail_path = os.path.join(getpathInfo.get_Path(), 'result', 'report.html')#获取测试报告路径
log = Logger(__name__)

path = getpathInfo.get_Path()
report_path = os.path.join(path, 'result')  # 存放测试报告文件的路径
mail_path = os.path.join(path,'testFile')#存放收件人地址文件路径
class send_email():
    '''
        邮件配置信息
        '''

    def __init__(self,
                 receiver,
                 subject='framfriend 系统测试报告',
                 server='smtp.qq.com',
                 fromuser='996941471@qq.com',
                 frompassword='yjkxwfmrbumrbbce',
                 sender='996941471@qq.com'):
        """
        :param receiver:
        :param subject:
        :param server:
        :param fromuser:
        :param frompassword:
        :param sender:
        """

        self._server = server
        self._fromuser = fromuser
        self._frompassword = frompassword
        self._sender = sender
        self._receiver = receiver
        self._subject = subject

    def sendEmail(self, fileName):
        """
        :param filename:
        :return:
        """
        #   打开报告文件读取文件内容
        try:
            f = open(os.path.join(report_path, fileName), 'rb')
            fileMsg = f.read()
        except Exception:
            log.logger.exception(
                'open or read file [%s] failed,No such file or directory: %s' % (fileName, report_path))
            log.logger.info('open and read file [%s] successed!' % fileName)
        else:
            f.close()
            #   邮件主题
            subject = 'Python test report'  #
            #   邮件设置
            msg = MIMEText(fileMsg, 'html', 'utf-8')
            msg['subject'] = Header(subject, 'utf-8')
            msg['from'] = self._sender
            #   连接服务器，登录服务器，发送邮件
            try:
                smtp = smtplib.SMTP()
                smtp.connect(self._server)
                smtp.login(self._fromuser, self._frompassword)
            except Exception:
                log.logger.exception('connect [%s] server failed or username and password incorrect!' % smtp)
            else:
                log.logger.info('email server [%s] login success!' % smtp)
                try:
                    smtp.sendmail(self._sender, self._receiver, msg.as_string())
                except Exception:
                    log.logger.exception('send email failed!')
                else:
                    log.logger.info('send email successed!')


#   从文件中读取邮件接收人信息
def getReceiverInfo(fileName):
    '''
    :param filename: 读取接收邮件人信息
    :return: 接收邮件人信息
    '''
    try:
        openFile = open(os.path.join(mail_path, fileName))
    except Exception:
        log.logger.exception('open or read file [%s] failed,No such file or directory: %s' % (fileName, mail_path))
    else:
        log.logger.info('open file [%s] successed!' % fileName)
        for line in openFile:
            msg = [i.strip() for i in line.split(',')]
            log.logger.info('reading [%s] and got receiver value is [%s]' % (fileName, msg))
            return msg


if __name__ == '__main__':# 运营此文件来验证写的send_email是否正确
    readMsg = getReceiverInfo('mail_receiver.txt')
    sendmail = send_email(readMsg)
    sendmail.sendEmail('report.html')