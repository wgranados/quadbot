import discord
import asyncio

from plugins.invoker import Invoker
from utils.details import config


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = kwargs['config']

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        for guild in self.guilds:
            print(guild.name)

    async def on_message(self, message):
        if message.author == self.user:
            return 
        if str(message.channel) in self.config['channels']:
            if message.content.startswith(self.config['command_prefix']):
                reply = await invoker.invoke_command(message)
                await message.channel.send(reply)
                # print(reply)


intents = discord.Intents.default()
intents.message_content = True
invoker = Invoker()
dsclient = MyClient(intents=intents, config=config['discord'])

