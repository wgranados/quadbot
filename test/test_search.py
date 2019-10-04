import asyncio
import aiohttp
import pytest
from plugins.search.SearchCommand import Search

# currently couping between pokemonshowdown client and this command is pretty 
# high so we need to import these for the time being to test functionality
from clients.pokemon.room import Room
from clients.pokemon.user import User

cmd = Search(searx_host='http://localhost:8888')

@pytest.mark.asyncio
async def test_search_github():
    testing_room = Room('test')
    testing_user = User('test', '@', True)
    res = await cmd.response(testing_room, testing_user, ['pokemon-showdown', 'github'])
    assert res.text == 'Pokémon battle simulator. - retrieved from https://github.com/Zarel/Pokemon-Showdown'

@pytest.mark.asyncio
async def test_search_steam():
    testing_room = Room('test')
    testing_user = User('test', '@', True)
    res = await cmd.response(testing_room, testing_user, ['dark souls', 'steam'])
    assert res.text == 'https://steamcdn-a.akamaihd.net/steam/apps/374320/capsule_sm_120.jpg?t=1553251330 - retrieved from https://store.steampowered.com/app/374320/DARK_SOULS_III/?snr=1_7_15__13'

@pytest.mark.asyncio
async def test_search_google():
    testing_room = Room('test')
    testing_user = User('test', '@', True)
    res = await cmd.response(testing_room, testing_user, ['pokemon', 'google'])
    assert res.text == 'The official source for Pokémon news and information on the Pokémon Trading Card Game, apps, video games, animation, and the Pokédex. - retrieved from https://www.pokemon.com/us/'