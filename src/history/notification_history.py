import json
import os
import ast


def write_config_bundles(new_data):
    try:
        #
        try:
            new_data = ast.literal_eval(new_data)
        except:
            new_data = new_data
        #
        with open(os.path.join(os.path.dirname(__file__), 'history.json'), 'w+') as output_file:
            output_file.write(json.dumps(new_data, indent=4, separators=(',', ': ')))
            output_file.close()
        #
        return True
    except Exception as e:
        return False


def get_cfg_bundles_json():
    with open(os.path.join(os.path.dirname(__file__), 'history.json'), 'r') as data_file:
        return json.load(data_file)


def get_child_history(child_id):
    data = get_cfg_bundles_json()
    return data[child_id]


def check_history(child_id, item_id):
    history = get_child_history(child_id).keys()
    return item_id in history


def add_history(child_id, item_id, title, notes, img_count, vid_count, date_observation, date_email):
    data = get_cfg_bundles_json()
    #
    data[child_id][item_id] = {}
    data[child_id][item_id]['title'] = title
    data[child_id][item_id]['notes'] = notes
    data[child_id][item_id]['img_count'] = img_count
    data[child_id][item_id]['vid_count'] = vid_count
    data[child_id][item_id]['date_observation'] = date_observation
    data[child_id][item_id]['date_email'] = date_email
    #
    write_config_bundles(data)
