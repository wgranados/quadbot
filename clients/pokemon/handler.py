import asyncio
from clients.pokemon.showdown import Client
from clients.pokemon.user import User
from clients.pokemon.showdown import ReplyObject
from plugins.invoker import Invoker
from utils.details import config

psclient = Client(config['pokemon-showdown'])
invoker = Invoker()

@psclient.event
async def chat_handler(message):
    # handle the command logic elsewhere elsewhere
    if message.requests_command():
        if message.is_pm:
            reply = await invoker.invoke_command(message)
            await psclient.send_pm(message.user.name, reply.text)
        # handle public room messages to avoid spam
        if not message.is_pm and User.compare_ranks(message.user.rank, message.room.broadcastrank):
            reply = await invoker.invoke_command(message)
            await psclient.send_room(message.room.name, reply.text)
        else:
            await psclient.send_pm(message.user.name, 'insufficient rank')

@psclient.event
async def battle_handler(message):
    pass