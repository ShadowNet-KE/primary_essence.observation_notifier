import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email import Encoders
from datetime import datetime

import config
from src.history.notification_history import add_history


def send_notifications_all(child_id, objObs):
    #
    count = 0
    #
    for objOb in objObs:
        result = email_observations(objOb)
        if result:
            add_history(child_id, objOb.id(),
                        objOb.title(), objOb.notes(),
                        len(objOb.imgs()),
                        len(objOb.vids()),
                        objOb.date_observation(),
                        datetime.now().strftime('%Y/%m/%d %H:%M'))
            count += 1
    #
    return count


def email_observations(objOb):
    #
    try:
        msg = compile_email(objOb)
        return send_email(msg)
    except Exception as e:
        print("ERROR sending email for {id}: {error}".format(id=objOb.id(), error=e))
        return False


def compile_email(objOb):
    #
    msg = MIMEMultipart('mixed')
    msg["To"] = '; '.join(config.get_config_notifications_emailto())
    msg["From"] = config.get_config_email_username()
    msg["Subject"] = 'Primary Essence: {title}'.format(title=objOb.title())
    #
    text = '{notes}<br><br>'.format(notes=objOb.notes())
    msgText = MIMEText(text, 'html')
    #
    msg.attach(msgText)
    #
    if objOb.imgs() > 0:
        i_count = 0
        for i in objOb.imgs():
            image_name = 'img_{id}_{count}.jpg'.format(id=objOb.id(), count=i_count)
            img = MIMEImage(i)
            img.add_header('Content-ID', '<{image}>'.format(image=image_name))
            msg.attach(img)
            i_count += 1
    #
    if objOb.vids() > 0:
        v_count = 0
        for v in objOb.vids():
            vid_name = 'vid_{id}_{count}.mp4'.format(id=objOb.id(), count=v_count)
            vid = MIMEBase('application', "octet-stream")
            vid.set_payload(v)
            Encoders.encode_base64(vid)
            vid.add_header('Content-Disposition', 'attachment; filename="%s"' % vid_name)
            msg.attach(vid)
            v_count += 1
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
                 config.get_config_notifications_emailto(),
                 msg.as_string())
    eml.quit()
    return True
