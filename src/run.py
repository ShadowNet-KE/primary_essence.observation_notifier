from time import sleep
import datetime
from primaryessence.get_data import get_learningJournal
from primaryessence.session import create_session
from primaryessence.parse_observations import find_observations
from notifications.notify_email import send_notifications_all
from notifications.error_email import send_error_email
from log.log import log_internal
from resources.global_resources.logs import logException, logPass
import config


err_count = 0
err_encountered = False


def get_next(now, err_encountered):
    #
    s = 7    # opening time of nursery in 24 hours
    e = 18   # closing time of nursery in 24 hours
    #
    if now.hour >= datetime.time(e).hour or err_encountered:
        nxt = datetime.datetime(now.year, now.month, now.day, datetime.time(s).hour, 0, 0, 0) + datetime.timedelta(days=1)
    elif now.hour < datetime.time(s).hour:
        nxt = datetime.datetime(now.year, now.month, now.day, datetime.time(s).hour, 0, 0, 0)
    else:
        nxt = now + datetime.timedelta(hours=1)
    #
    return nxt


while True:
    #
    now = datetime.datetime.now()
    #
    log_internal(logPass, 'Operation started')
    #
    try:
        s = create_session(config.get_config_primaryessence_nursery(),
                           config.get_config_primaryessence_prefix(),
                           config.get_config_primaryessence_username(),
                           config.get_config_primaryessence_password())
        #
        count = 0
        #
        r = {}
        o = {}
        for child_id in config.get_config_primaryessence_childids():
            r[child_id] = get_learningJournal(s, child_id)
            o[child_id] = find_observations(s, r[child_id], child_id)
            #
            count += send_notifications_all(child_id, o[child_id])
        #
        log_internal(logPass, 'Operation completed successfully:  {count} email updates found'.format(count=count))
        #
        err_count = 0
        err_encountered = False
        #
    except Exception as e:
        err_count =+ 1
        if err_count > 4:
            err_encountered = True
            send_error_email()
            log_internal(logException, 'scheduled operation',
                         description='Error running operation: Error limit reached',
                         exception=e)
        else:
            log_internal(logException, 'scheduled operation',
                         description='Error running operation: Attempt {err_count}'.format(err_count=err_count),
                         exception=e)
    #
    nxt = get_next(now, err_encountered)
    #
    log_internal(logPass, 'Next scheduled run will be: {dt}'.format(dt=nxt.strftime('%Y-%m-%d %H:%M')))
    #
    #
    slp = (nxt - now).seconds
    #
    sleep(slp)
    #
