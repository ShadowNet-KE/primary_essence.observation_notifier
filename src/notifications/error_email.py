import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import creds


def send_error_email():
    msg = compile_error_email()
    send_email(msg)


def compile_error_email():
    #
    msg = MIMEMultipart()
    msg["To"] = '; '.join(creds.ERR_EML_TO)
    msg["From"] = creds.USERNAME
    msg["Subject"] = 'Primary Essence: ERROR LIMIT REACHED'
    #
    text = 'Error limit reached. An attempt will next be made tomorrow, however it is advised to check the application to investigate the error.'
    #
    msgText = MIMEText(text, 'html')
    msg.attach(msgText)
    #
    return msg


def send_email(msg):
    eml = smtplib.SMTP(creds.SERVER, creds.PORT)
    eml.starttls()
    eml.set_debuglevel(0)
    eml.login(creds.USERNAME, creds.PASSWORD)
    eml.sendmail(creds.USERNAME, creds.ERR_EML_TO, msg.as_string())
    eml.quit()
    return True
