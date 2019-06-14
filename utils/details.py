import yaml
import re
import os

ps_config = {}
discord_config = {}
apikeys = {}

def to_id(thing):
    """Assigns a unique ID to everyone"""
    return re.sub(r'[^a-zA-z0-9,]', '', thing).lower()

class DetailsNotFoundError(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return 'Details could not be loaded because:' + self.reason

def load_config(path):
    """Attempts to load details from the given path."""
    global ps_config
    global discord_config
    global apikeys
    try:
        with open(path, 'r') as yaml_file:
            config = yaml.load(yaml_file)
            ps_config = config['ps_config']
            ps_config['bot_id'] = to_id(ps_config['bot_username'])
            discord_config = config['discord_config']
            apikeys = config['apikeys']
    except FileNotFoundError as e:
        raise DetailsNotFoundError('details.yaml not found')

def load_travis_config():
    """Attempts to load details required for a Travis CI build test"""
    global ps_config
    global discord_config
    try:
        ps_config['bot_username'] = 'quadbot'
        ps_config['master'] = 'wgma'
        ps_config['bot_login'] = ''
        ps_config['bot_id'] = to_id(details['bot_username'])
        ps_config['command_char'] = '.'
        ps_config['avatar'] = 0
        ps_config['joinRooms'] = {}
        ps_config['apikeys'] = {'imgur': os.environ['IMGUR_API']}
    except Exception as e:
        raise DetailsNotFoundError('environment variables not set on Travis')

def init():
    try:
        load_config('details.yaml')
    except FileNotFoundError as e:
        load_travis_defaults()
if __name__ == '__main__':
    init()
