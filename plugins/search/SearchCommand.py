# curl localhost:8888 --data 'q=yeet&format=json' 
import asyncio
from plugins.CommandBase import CommandBase
from showdown.showdown import ReplyObject

class Search(CommandBase):
  def __init__(self):
    pass

  async def response(self, room, user, args):
    return await asyncio.sleep(0)
