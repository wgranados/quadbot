import sys
import time
import asyncio
from utils.details import config

from clients.pokemon.handler import psclient
from clients.discord.handler import dsclient
#from showdown.event_handler import psclient
# from discord.event_handler import dsclient

if __name__ == "__main__":
    supported_platforms = ['discord', 'pokemon-showdown', 'slack']
    if len(sys.argv) != 2:
        print('serve [platform]\n \t platform: string, one of {}'.format(','.join(supported_platforms)))
        exit(0)


    platform = sys.argv[1]
    if platform not in supported_platforms:
        print('%s is not supported'.format(platform))
        exit(0)
    
    if platform == 'pokemon-showdown':
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(psclient.make_connection())
    elif platform == 'discord':
        dsclient.run(config['discord']['token'])
    elif platform == 'slack':
        pass
