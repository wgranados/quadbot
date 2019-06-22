# curl localhost:8888 --data 'q=yeet&format=json' 
import asyncio
import aiohttp
import json
from plugins.CommandBase import CommandBase
from utils.details import config
from clients.pokemon.showdown import ReplyObject

class Search(CommandBase):
  def __init__(self):
    super().__init__(aliases=['search'], can_learn=False)
    self.supported_engines = [
      'google',
      'steam',
      'github'
      ]

  def learn(self, room, user, data):
        pass

  async def query(self, search_term, engines):
    """queries searx for info.
    
    args:
      search_term: string, something being searched for.
      engines: string, specific engines supported.
    """
    session = aiohttp.ClientSession()
    url = 'http://searx:8888'
    payload = {'q': search_term , 'format':'json', 'engines': engines}
    resp = await session.get(url, data=payload)
    text = await resp.text()
    val = json.loads(text)
    await session.close()
    return val 
    """queries searx for info.
    
    args:
      search_term: string, something being searched for.
      engines: string, specific engines supported.
    """
    session = aiohttp.clientsession()
    url = 'http://searx:8888'
    payload = {'q': search_term , 'format':'json', 'engines': engines}
    resp = await session.get(url, data=payload)
    text = await resp.text()
    val = json.loads(text)
    await session.close()
    return val 

  async def response(self, room, user, args):
        if len(args) == 1 and args[0] == 'help':
            return ReplyObject('{}/{}'.format(config['base-url'], self.aliases[0])) 
        elif len(args) > 3:
            return ReplyObject('Too many arguments provided.')
        elif len(args) == 0:
            return ReplyObject('Not enough arguments provided.')
        elif len(args) >= 2 and args[1] not in self.supported_engines:
            return ReplyObject('engine provided not supported')
        else:
            return await self._success(room, user, args)


  def _help(self, room, user, args):
    pass

  async def _success(self, room, user, args):
      """ Returns a success response to the user.

      Successfully returns the expected response from the user based on the args.

      Args:
          room: Room, room this command was evoked from.
          user: User, user who evoked this command.
          args: list of str, any sequence of parameters which are supplied to this command
      Returns:
          ReplyObject
      """
      if len(args) == 1:
        search = args[0]
        q = await self.query(search)
        if q['results']:
          url = q['results'][0]['pretty_url']
          content = q['results'][0]['content']
          rep = '{} - retrieved from {}'.format(content, url)
          return ReplyObject(rep, True) if len(rep) <= 300 else ReplyObject(rep[:300], True)
        else:
          return ReplyObject('Your query didn\'t come up with results')
      elif len(args) == 2:
        search, engine = args[0], args[1]
        q = await self.query(search, engine)
        if q['results']:
          url = q['results'][0]['pretty_url']
          content = q['results'][0]['content']
          rep = '{} - retrieved from {}'.format(content, url)
          return ReplyObject(rep, True) if len(rep) <= 300 else ReplyObject(rep[:300], True)
        else:
          return ReplyObject('Your query didn\'t come up with results')
      elif len(args) == 3: 
        search, engine, limit = args[0], args[1], int(args[2])
        q = await self.query(search, engine)
        if q['results']:
          reply = []
          for i in range(min(len(q['results']), limit)):
            url, content = q['results'][i]['pretty_url'], q['results'][i]['content']
            rep = '{} - retrieved from {}'.format(content, url)
            reply.append(rep if len(rep) <= 300 else rep[:300])
          return ReplyObject('\n'.join(reply))
        else:
          return ReplyObject('Your query didn\'t come up with results')
