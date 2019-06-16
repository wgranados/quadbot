import sys
from showdown.showdown import Client
import asyncio
from plugins.invoker import Invoker
from showdown.showdown import ReplyObject
from utils.details import config

invoker = Invoker()
psclient = Client(config['pokemon-showdown'])

@psclient.event
async def chat_handler(message):
    # handle the command logic elsewhere elsewhere
    if message.requests_command():
        reply = await invoker.invoke_command(message)
        if not message.is_pm:
            await psclient.send_room(message.room.name, reply.text)
        else:
            await psclient.send_pm(message.user.name, reply.text)

@psclient.event
async def battle_handler(message):
    pass


if __name__ == "__main__":
    supported_platforms = ['discord', 'pokemon-showdown', 'slack']
    platform = sys.argv[1]
    if(len(sys.argv) < 2 or platform not in supported_platforms):
        print('serve [platform]\n \t platform: string, one of {}'.format(','.join(supported_platforms)))
        exit(0)
    if platform == 'pokemon-showdown':
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(psclient.make_connection())
    elif platform == 'discord':
        pass
    elif platform == 'slack':
        pass
