import yaml
import re
import os

config = {}
structure = {
    'pokemon-showdown' :  {
        'username': '',
        'password': '',
        'owner': '',
        'command_prefix': '',
        'avatar': 0,
        'rooms': []
    }, 
    'discord' : {
        'command_prefix': '',
        'token' : '',
        'channels' : ['bots']
    }
}

class DetailsError(Exception):
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return 'Details could not be loaded because:' + self.reason

def load_config(path):
    """Attempts to load details from the given path."""
    global config
    try:
        with open(path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            if not config['pokemon-showdown'] or config['pokemon-showdown'].keys() != structure['pokemon-showdown'].keys():
                raise DetailsError('details.yaml structure incorrect, check details.py for correct structure')
            if not config['discord'] or config['discord'].keys() != structure['discord'].keys():
                raise DetailsError('details.yaml structure incorrect, check details.py for correct structure')
    except FileNotFoundError as e:
        raise DetailsError('details.yaml not found')

def init():
    load_config('details.yaml')

init()
