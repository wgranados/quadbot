import asyncio
import aiohttp
import json
from plugins.CommandBase import CommandBase
from utils.images import OnlineImage
from showdown.showdown import ReplyObject
from showdown.Users import User 

class Steam(CommandBase):
  def __init__(self):
    super().__init__(aliases=['steam'], can_learn=False)

  def learn(self, room, user, data):
        pass

  async def query(self, search_term, engines='steam'):
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

  async def get_game_data(self, gameid):
    session = aiohttp.ClientSession()
    game_url = 'https://store.steampowered.com/app/{}'.format(gameid) 
    payload= {'appids': gameid}
    resp = await session.get('http://store.steampowered.com/api/appdetails', params=payload)
    text = await resp.text()
    game_data = json.loads(text)[gameid]['data']
    header_image, name, desc = game_data['header_image'], game_data['name'], game_data['short_description']
    return game_url, header_image, name, desc

  def parse_gameid(self, url):
    count = 0
    gameid = []
    for char in url: 
      if char == '/':
        count += 1 
        continue
      if count == 4:
        gameid.append(char)
    return ''.join(gameid)

  async def response(self, room, user, args):
    if len(args) == 1 and args[0] == 'help':
        return ReplyObject('{}/{}'.format(config['base-url'], self.aliases[0])) 
    elif len(args) > 2:
        return ReplyObject('Too many arguments provided.')
    elif len(args) == 0:
        return ReplyObject('Not enough arguments provided.')
    else:
        return await self._success(room, user, args)

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
      search = args[0]
      show_image = args[-1] == 'showimage' if args else False
      q = await self.query(search)
      if q['results']:
        url = q['results'][0]['url']
        content = q['results'][0]['content']
        gameid = self.parse_gameid(url) 
        header_image, name, description = await self.get_game_data(gameid)
        width, height = OnlineImage.get_image_info(header_image)
        if User.compareRanks(room.rank, '*') and show_image:
            return ReplyObject(('/addhtmlbox <div id="gameinfo"> <img src="{}" height="{}" width="{}"></img> <p>Name: <a href="{}"> {}</a></p> <p>Description: {} </p> </div>').format(header_image, height, width, game_url, name, description), True, True)
        else:
            return ReplyObject('Name: {} Link: Description: {}'.format(name, game_url, description), True)
      else:
        return ReplyObject('Your query didn\'t come up with results')
