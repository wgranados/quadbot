import discord
import asyncio

from plugins.invoker import Invoker
from utils.details import config


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = kwargs['config']
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

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

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(137356419333750784) # channel ID goes here
        while not self.is_closed():
            counter += 1
            await asyncio.sleep(60) # task runs every 60 seconds

invoker = Invoker()
dsclient = MyClient(config=config['discord']) 

