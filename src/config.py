import json
import os


def get_cfg_bindings_json():
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as data_file:
        data = json.load(data_file)
    return data['config']

################################################################################################
# Email
################################################################################################

def get_config_email():
    data = get_cfg_bindings_json()
    return data['email']


def get_config_email_server():
    data = get_config_email()
    return data['SERVER']


def get_config_email_port():
    data = get_config_email()
    return data['PORT']


def get_config_email_username():
    data = get_config_email()
    return data['USERNAME']


def get_config_email_password():
    data = get_config_email()
    return data['PASSWORD']

################################################################################################
# Primary Essence
################################################################################################

def get_config_primaryessence():
    data = get_cfg_bindings_json()
    return data['primary_essence']


def get_config_primaryessence_prefix():
    data = get_config_primaryessence()
    return data['PREFIX']


def get_config_primaryessence_username():
    data = get_config_primaryessence()
    return data['USERNAME']


def get_config_primaryessence_password():
    data = get_config_primaryessence()
    return data['PASSWORD']


def get_config_primaryessence_nursery():
    data = get_config_primaryessence()
    return data['NURSERY']


def get_config_primaryessence_childids():
    data = get_config_primaryessence()
    return data['CHILD_ID']

################################################################################################
# Notifications
################################################################################################

def get_config_notifications():
    data = get_cfg_bindings_json()
    return data['notifications']


def get_config_notifications_emailto():
    data = get_config_notifications()
    return data['EML_TO']


def get_config_notifications_erroremail():
    data = get_config_notifications()
    return data['ERR_EML_TO']
