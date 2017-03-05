import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import creds
from notification_history import check_history, add_history

EML_TO = 'robe16@hotmail.co.uk'


def send_notifications_all(child_id, objObs):
    #
    for objOb in objObs:
        if not check_history(child_id, objOb.id()):
            email_observations(objOb)
            add_history(child_id, objOb.id())


def email_observations(objOb):
    #
    try:
        msg = compile_email(objOb)
        return send_email(msg)
    except Exception as e:
        return False


def compile_email(objOb):
    image_name = 'img_{id}.jpg'.format(id=objOb.id())
    #
    msg = MIMEMultipart()
    msg["To"] = EML_TO
    msg["From"] = creds.USERNAME
    msg["Subject"] = 'Primary Essence: {title}'.format(title=objOb.title())
    #
    msgText = MIMEText('<b>{body}</b><br><img src="cid:{img}"><br>'.format(body=objOb.comment(), img=image_name), 'html')
    msg.attach(msgText)
    #
    img = MIMEImage(objOb.img())
    img.add_header('Content-ID', '<{image}>'.format(image=image_name))
    msg.attach(img)
    #
    return msg


def send_email(msg):
    eml = smtplib.SMTP(creds.SERVER, creds.PORT)
    eml.starttls()
    eml.set_debuglevel(1)
    eml.login(creds.USERNAME, creds.PASSWORD)
    eml.sendmail(creds.USERNAME, EML_TO, msg.as_string())
    eml.quit()
    return True
