import urllib
import urllib2
import conf
from random import randint
from boto3.dynamodb.conditions import Key, Attr
from multiprocessing.dummy import Pool
from database_manager import BopBotDatabase
import json


interactive_buttons = {
    'menu_event': ['Send the poll', 'More options'],
    'menu_event_general': [],
    'reminder_menu': ['Set reminder', 'No thanks'],
    'archive_channel': ['Archive', 'Later'],
    'simple_demo_start': ['Simple demo'],
    'simple_demo_more_options': ['More options'],
    'simple_demo_send_the_poll': ['Send the poll']
}

user_status = {
    'tutorial': {
        'command_def': {
            'wte': {
                'module': '',
                'function': 'start_what_to_eat_flow',
                'parameters': ['bot_token', 'user_id', 'access_token']
            },
            'stop': {
                'module': '',
                'function': 'send_stop_message_with_key',
                'parameters': ['key=error_4', 'bot_token', 'user_id']
            },
            'demo': {
                'module': '',
                'function': 'send_simple_message_to_slack_with_key',
                'parameters': ['key=error_6', 'bot_token', 'user_id']
            },
        },
        'else': {
            'module': '',
            'function': 'send_simple_message_to_slack_with_key',
            'parameters': ['key=error_7', 'bot_token', 'user_id']
        }
    },

    'wte_location_input': {
        'command_def': {
            'wte': {
                'module': '',
                'function': 'send_simple_message_to_slack_with_key',
                'parameters': ['key=error_3', 'bot_token', 'user_id']
            },
            'stop': {
                'module': '',
                'function': 'send_stop_message_with_key',
                'parameters': ['key=error_4', 'bot_token', 'user_id']
            },
            'demo': {
                'module': 'bopbot_tutorial',
                'function': 'send_start_demo_message',
                'parameters': ['user_id', 'bot_token']
            },
            'mymusictaste': {
                'module': '',
                'function': 'send_random_restaurant_list',
                'parameters': ['location=mymusictastehq', 'user_id', 'bot_token']
            }
        },
        'else': {
            'module': '',
            'function': 'process_wte_location_input',
            'parameters': ['bot_token', 'user_id', 'user_command']
        }
    },

    'wte_location_choice': {
        'command_def': {
            'wte': {
                'module': '',
                'function': 'send_simple_message_to_slack_with_key',
                'parameters': ['key=error_3', 'bot_token', 'user_id']
            },
            'stop': {
                'module': '',
                'function': 'send_stop_message_with_key',
                'parameters': ['key=error_4', 'bot_token', 'user_id']
            },
            'demo': {
                'module': 'bopbot_tutorial',
                'function': 'send_start_demo_message',
                'parameters': ['user_id', 'bot_token']
            },
        },

        'else': {
            'module': '',
            'function': 'process_wte_location_choice',
            'parameters': ['bot_token', 'user_id', 'user_command']
        }
    },

    'wte': {
        'command_def': {
            'wte': {
                'module': '',
                'function': 'send_simple_message_to_slack_with_key',
                'parameters': ['key=error_3', 'bot_token', 'user_id']
            },
            'stop': {
                'module': '',
                'function': 'send_stop_message_with_key',
                'parameters': ['key=error_4', 'bot_token', 'user_id']
            },
            'demo': {
                'module': 'bopbot_tutorial',
                'function': 'send_start_demo_message',
                'parameters': ['user_id', 'bot_token']
            },
        },
        'else': {
            'module': '',
            'function': 'send_simple_message_to_slack_with_key',
            'parameters': ['key=error_9', 'bot_token', 'user_id']
        }
    },

    'wte_invitation': {
        'command_def': {
            'wte': {
                'module': '',
                'function': 'send_simple_message_to_slack_with_key',
                'parameters': ['key=error_3', 'bot_token', 'user_id']
            },
            'stop': {
                'module': '',
                'function': 'send_stop_message_with_key',
                'parameters': ['key=error_4', 'bot_token', 'user_id']
            },
            'demo': {
                'module': 'bopbot_tutorial',
                'function': 'send_start_demo_message',
                'parameters': ['user_id', 'bot_token']
            },
        },
        'else': {
            'module': '',
            'function': 'process_wte_invitation',
            'parameters': ['bot_token', 'user_id', 'user_command', 'access_token']
        }
    },

    'poll': {
        'command_def': {
            'wte': {
                'module': '',
                'function': 'start_what_to_eat_flow',
                'parameters': ['bot_token', 'user_id', 'access_token']
            },
            'stop': {
                'module': '',
                'function': 'send_simple_message_to_slack_with_key',
                'parameters': ['key=error_5', 'bot_token', 'user_id']
            },
            'demo': {
                'module': '',
                'function': 'send_simple_message_to_slack_with_key',
                'parameters': ['key=error_2', 'bot_token', 'user_id']
            },
        },
        'else': {
            'module': '',
            'function': 'send_simple_message_to_slack_with_key',
            'parameters': ['key=error_1', 'bot_token', 'user_id']
        }
    },

    'reminder': {
        'command_def': {
            'wte': {
                'module': '',
                'function': 'start_what_to_eat_flow',
                'parameters': ['bot_token', 'user_id', 'access_token']
            },
            'stop': {
                'module': '',
                'function': 'send_simple_message_to_slack_with_key',
                'parameters': ['key=error_6', 'bot_token', 'user_id']
            },
            'demo': {
                'module': 'bopbot_tutorial',
                'function': 'send_start_demo_message',
                'parameters': ['user_id', 'bot_token']
            },
        },
        'else': {
            'module': '',
            'function': 'send_reminder_process',
            'parameters': ['bot_token', 'user_id', 'user_command', 'access_token']
        }
    },

    'normal': {
        'command_def': {
            'wte': {
                'module': '',
                'function': 'start_what_to_eat_flow',
                'parameters': ['bot_token', 'user_id', 'access_token']
            },
            'stop': {
                'module': '',
                'function': 'send_simple_message_to_slack_with_key',
                'parameters': ['key=error_1', 'bot_token', 'user_id']
            },
            'demo': {
                'module': 'bopbot_tutorial',
                'function': 'send_start_demo_message',
                'parameters': ['user_id', 'bot_token']
            },
            'hi': {
                'module': '',
                'function': 'send_simple_message_to_slack_with_key',
                'parameters': ['key=hi', 'bot_token', 'user_id']
            }
        },
        'else': {
            'module': '',
            'function': 'send_simple_message_to_slack_with_key',
            'parameters': ['key=error_1', 'bot_token', 'user_id']
        }
    }
}

wte_status = [
    'tutorial',
    'poll',
    'reminder'
]

stop_status = [

]

wte_commands = [
    'whattoeat',
    'whattoeat?',
    'bopbot'
]


def get_dict_for_slack_post_request(token, channel, text=None, attachments=None, as_user='true'):
    """
    return dictionary for slack chat post request
    :param token: bot users token
    :param channel: channel that message will be sent
    :param text: text that will be sent
    :param attachments: list of attachment
    :param as_user: if true message will be sent as bot user, if false message will be sent as slack app.
    :return:
    """
    payload = {'token': token, 'channel': channel, 'as_user': as_user}
    if text:
        payload.update({'text': text})

    if attachments:
        payload.update({'attachments': attachments})

    return payload


def make_bopbot_request_result_dict(is_success, parameter):
    return {'success': is_success, 'result': parameter}


def im_open(user_id, bot_token):
    """
    send im.open request to slack server
    :param user_id:
    :param bot_token:
    :return:
    """
    url = 'https://slack.com/api/im.open'
    payload = {'token': bot_token, 'user': user_id}
    return send_request(url, payload)


def get_phrase(key):
    """
    get bopbot phrase
    :param key: key for phrase
    :return: bopbot request result dictionary
    """
    try:
        phrases_table = BopBotDatabase(table=conf.BOT_PHRASES)
        query = Key('Key').eq(key)

        items = phrases_table.query_items_from_table(query=query)

        if len(items) > 1:
            index = randint(0, len(items)-1)
            phrase = items[index]['Phrase'].encode('utf8')
        else:
            phrase = items[0]['Phrase'].encode('utf8')

        return phrase
    except Exception, e:
        raise Exception('Bad Request: Exception: %s' % e)


def send_request_to_slack(url, parameter=None):
    """
    send request
    :param url: url for request
    :param parameter: parameter for request
    :return:
    """
    try:
        if parameter:
            data = urllib.urlencode(parameter, doseq=True)
            req = urllib2.Request(url, data)
        else:
            req = urllib2.Request(url)

        response = urllib2.urlopen(req).read()
        response = json.loads(response)
        print response

        if not response['ok']:
            return False
        else:
            return response

    except Exception, e:
        print e
        return False


def send_request(url, parameter=None):
    """
    send request
    :param url: url for request
    :param parameter: parameter for request
    :return:
    """
    try:
        if parameter:
            data = urllib.urlencode(parameter, doseq=True)
            req = urllib2.Request(url, data)
        else:
            req = urllib2.Request(url)

        response = urllib2.urlopen(req).read()

        return response
    except Exception, e:
        print e
        return False


def send_request_wrapper(args):
    """
    wrapper for request
    :param args: set of param (url, parameter)
    :return:
    """
    return send_request_to_slack(*args)


def send_request_with_multiprocessing_pool(processes, params):
    """
    send multiple http requests with multiprocessing pool
    :param processes: number of process
    :param params: list of parameter for each request.
    :return:
    """
    pool = Pool(processes)
    try:
        results = pool.map(send_request_wrapper, params)
        return make_bopbot_request_result_dict(True, results)
    except Exception, e:
        return make_bopbot_request_result_dict(False, e)


def make_im_button_attachment(callback_id, actions, color='#3aa3e3', text=None):
    """
    make button attachments for interactive messages
    :param text: attachment text
    :param callback_id: callback_id
    :param actions: list of action
    :param color: attachment color
    :return: attachment dictionary
    """
    attachment = {
        'color': color,
        'attachment_type': 'default',
        'fallback': callback_id,
        'callback_id': callback_id,
        'actions': actions
    }

    if text:
        attachment.update({'text': '%s' % text})

    return attachment


def make_restaurant_list_attachments(restaurant_list):
    """
    make attachment list of restaurant
    :param restaurant_list:
    :return:
    """
    attachments = []
    for restaurant in restaurant_list:
        categories = restaurant['categories']
        categories_text = str()
        for index, category in enumerate(categories):
            if index < 3:
                if index == 0:
                    categories_text += category['name'].encode('utf8')
                else:
                    categories_text += ', ' + category['name'].encode('utf8')

        attachment = {
            'title': restaurant['name'].encode('utf8'),
            'title_link': restaurant['url'].encode('utf8'),
            'text': categories_text,
            'thumb_url': restaurant['image_url'],
            'color': '#3aa3e3'
        }
        attachments.append(attachment)

    return attachments


def make_im_button(name, text, value):
    return {'name': name, 'text': text, 'type': 'button', 'value': value}


def make_archive_payload(bot_token, user_id, channel):
    attachments = []
    phrase = get_phrase('reminder_archive') % channel
    actions = []
    for button in interactive_buttons['archive_channel']:
        action = make_im_button(name=button, text=button, value=channel)
        actions.append(action)

    attachments.append(make_im_button_attachment(callback_id='archive_channel', actions=actions))
    attachments = json.dumps(attachments)
    return get_dict_for_slack_post_request(token=bot_token, channel=user_id, text=phrase, attachments=attachments)