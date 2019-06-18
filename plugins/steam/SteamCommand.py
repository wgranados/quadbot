# curl 'http://localhost:8888/?q=dark+souls&engines=steam&format=json'
import asyncio
import aiohttp
import json
from plugins.CommandBase import CommandBase
from showdown.showdown import ReplyObject

class Steam(CommandBase):
  def __init__(self):
    super().__init__(aliases=['steam'], can_learn=False)

  def learn(self, room, user, data):
        pass

  async def query(self, search_term):
    session = aiohttp.ClientSession()
    url = 'http://searx:8888'
    payload = {'q': search_term , 'engines': 'steam', 'format':'json'}
    resp = await session.get(url, data=payload)
    text = await resp.text()
    val = json.loads(text)
    await session.close()
    return val 

  async def response(self, room, user, args):
    q = await self.query(args[0])
    return ReplyObject(q['results'][1]['url'])
      # can't directly convert to json since PS returns a weird format like
      # ']{json content}', so have to offset it by 1

  def _help(self, room, user, args):
    pass

  def _error(self, room, user, reason):
    pass

  def _success(self, room, user, args):
      """ Returns a success response to the user.

      Successfully returns the expected response from the user based on the args.

      Args:
          room: Room, room this command was evoked from.
          user: User, user who evoked this command.
          args: list of str, any sequence of parameters which are supplied to this command
      Returns:
          ReplyObject
      """
      pass
