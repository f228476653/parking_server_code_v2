# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.message import EmailMessage
from app.services.systemlog_service import SystemlogService
# Import the email modules we'll need
from email.parser import Parser
from email.mime.text import MIMEText
from email.header import Header


class EmailService:
    """ every thing about user , like account, permission, role"""
    _db = None
    _log_service = None
    _syslog = None
    _user = None
    _smpt = None
    _port = None
    def __init__(self, db, user):
        self._db = db
        self._user =user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}
        self._smpt = 'smtp.gmail.com'
        self._port = 587

    def send_pure_email(self , from_mail , from_mail_pwd ,to_mail , to_name ,msgText ,subject):
        smtpObj = smtplib.SMTP(self._smpt, self._port)
        smtpObj.starttls()
        smtpObj.login(from_mail , from_mail_pwd)#第一個參數是電郵帳號，第二個參數是密碼
        to = [to_mail,'yuhsiu.chang@acerits.com']  #收件者的電郵地址，為list資料型態
        msg = MIMEText(msgText, 'plain', 'utf-8')
        msg['From'] = Header("PMS+系統管理員", 'utf-8')
        msg['To'] =  Header(to_name, 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        smtpObj.sendmail(from_mail, to, msg.as_string())#利用sendmail 這個method 來寄出電郵，SMTP.sendmail(from_addr, to_addrs, msg, mail_options=[], rcpt_options=[])
        smtpObj.quit()  #關閉本地端對遠端郵件伺服器的連線


    def send_email(self):
        # If the e-mail headers are in a file, uncomment these two lines:
        # with open(messagefile) as fp:
        #     headers = Parser().parse(fp)

        #  Or for parsing headers in a string, use:
        headers = Parser().parsestr('From: <yuhsiu.chang@acerits.com>\n'
                'To: <huilong494@gmail.com>\n'
                'Subject: Test message\n'
                '\n'
                'Body would go here\n')

        #  Now the header items can be accessed as a dictionary:
        print('To: %s' % headers['to'])
        print('From: %s' % headers['from'])
        print('Subject: %s' % headers['subject'])
