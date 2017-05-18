import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email import Encoders

import creds
from src.history.notification_history import add_history


def send_notifications_all(child_id, objObs):
    #
    count = 0
    #
    for objOb in objObs:
        result = email_observations(objOb)
        if result:
            add_history(child_id, objOb.id())
            count += 1
    #
    return count


def email_observations(objOb):
    #
    try:
        msg = compile_email(objOb)
        return send_email(msg)
    except Exception as e:
        return False


def compile_email(objOb):
    #
    msg = MIMEMultipart()
    msg["To"] = '; '.join(creds.EML_TO)
    msg["From"] = creds.USERNAME
    msg["Subject"] = 'Primary Essence: {title}'.format(title=objOb.title())
    #
    # msgText = MIMEText('<b>{body}</b><br><img src="cid:{img}"><br>'.format(body=objOb.comment(), img=image_name), 'html')
    msgText = MIMEText('<b>{body}</b><br>'.format(body=objOb.comment()), 'html')
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
    eml = smtplib.SMTP(creds.SERVER, creds.PORT)
    eml.starttls()
    eml.set_debuglevel(0)
    eml.login(creds.USERNAME, creds.PASSWORD)
    eml.sendmail(creds.USERNAME, creds.EML_TO, msg.as_string())
    eml.quit()
    return True
