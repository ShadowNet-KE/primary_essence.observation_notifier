import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email import Encoders
from datetime import datetime
from log.log import log_internal
from resources.global_resources.logs import logException

import config
from history.notification_history import add_history


def send_notifications_all(child_id, objObs):
    #
    count = 0
    #
    for objOb in objObs:
        try:
            result = email_observations(objOb)
        except smtplib.SMTPDataError as e:
            log_internal(logException, 'scheduled operation',
                         description='Error sending email for {id}'.format(id=objOb.id()),
                         exception=e)
            raise Exception
        except Exception as e:
            log_internal(logException, 'scheduled operation',
                         description='Error sending email for {id}'.format(id=objOb.id()),
                         exception=e)
            result = False
        if result:
            add_history(child_id, objOb.id(),
                        objOb.title(),
                        objOb.comment(), objOb.commentby(),
                        objOb.aol_html(),
                        len(objOb.imgs()),
                        len(objOb.vids()),
                        objOb.date_observation(),
                        datetime.now().strftime('%Y/%m/%d %H:%M'))
            count += 1
    #
    return count


def email_observations(objOb):
    msg = compile_email(objOb)
    return send_email(msg)


def compile_email(objOb):
    #
    msg = MIMEMultipart('mixed')
    msg["To"] = '; '.join(config.get_config_notifications_emailto())
    msg["From"] = config.get_config_email_username()
    msg["Subject"] = 'Primary Essence: {title}'.format(title=objOb.title().encode('utf-8'))
    #
    text = ''
    #
    text += '<h2>{title}</h2>'.format(title=objOb.title())
    #
    if not objOb.comment() == '':
        text += '<h3>Comments</h3>'
        text += '<p>{comment}</p>'.format(comment=objOb.comment().encode('utf-8'))
        #
        text += '<p><b>Comment By:</b> {commentby}</p><br>'.format(commentby=objOb.commentby().encode('utf-8'))
    else:
        text += '<p><i>No \'Comments\' attached</i></p>'
    #
    if not objOb.aol_html() == '':
        text += '<h3>Aspects of Learning</h3>'
        text += '<p>{aol}</p>'.format(aol=objOb.aol_html().encode('utf-8'))
    else:
        text += '<p><i>No \'Aspects of Learning\' attached</i></p>'
    #
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
