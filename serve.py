import sys
import showdown
import discord
from discord.ext import commands
import asyncio
from plugins.invoker import Invoker
from showdown.showdown import ReplyObject

invoker = Invoker()

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
    if(sys.argc < 2 or sys.argv[0] not in supported_platforms):
        print('serve [platform]\n \t platform: string, one of {}'.format(','.join(supported_platforms)))
    platform = sys.argv[0] 
    if platform == 'pokemon-showdown':
        psclient = showdown.Client()
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(psclient.make_connection())
    elif platform == 'discord':
        bot.run('token')
    elif platform == 'slack':
        pass
