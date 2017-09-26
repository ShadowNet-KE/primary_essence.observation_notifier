import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config


def send_error_email():
    msg = compile_error_email()
    send_email(msg)


def compile_error_email():
    #
    msg = MIMEMultipart()
    msg["To"] = '; '.join(config.get_config_notifications_erroremail())
    msg["From"] = config.get_config_email_username()
    msg["Subject"] = 'Primary Essence: ERROR LIMIT REACHED'
    #
    text = 'Error limit reached. An attempt will next be made tomorrow, however it is advised to check the application to investigate the error.'
    #
    msgText = MIMEText(text, 'html')
    msg.attach(msgText)
    #
    return msg


def send_email(msg):
    eml = smtplib.SMTP(config.get_config_email_server(),
                       config.get_config_email_port())
    eml.starttls()
    eml.set_debuglevel(0)
    eml.login(config.get_config_email_username(),
              config.get_config_email_password())
    eml.sendmail(config.get_config_email_username(),
                 config.get_config_notifications_erroremail(),
                 msg.as_string())
    eml.quit()
    return True
