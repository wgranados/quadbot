# Copyright (C) 2016 William Granados<wiliam.granados@wgma00.me>
#
# This file is part of PokemonShowdownBot.
#
# PokemonShowdownBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PokemonShowdownBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PokemonShowdownBot.  If not, see <http://www.gnu.org/licenses/>.
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#     The MIT License (MIT)
#
#     Copyright (c) 2015 QuiteQuiet<https://github.com/QuiteQuiet>
#
#     Permission is hereby granted, free of charge, to any person obtaining a
#     copy of this software and associated documentation files (the "Software")
#     , to deal in the Software without restriction, including without
#     limitation the rights to use, copy, modify, merge, publish, distribute
#     sublicense, and/or sell copies of the Software, and to permit persons to
#     whom the Software is furnished to do so, subject to the following
#     conditions:
#
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#     OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#     CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#     TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#     SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Each PS room joined creates an object here.
# Objects control settings on a room-per-room basis, meaning every room can
# be treated differently.

from user import User


class Room:
    """ Contains all important information of a pokemon showdown room.

    Attributes:
        name: string, name of this room.
        room_setting: dict, dictionary containing a lot of the room settings in this room
                      defined below:
                      room_setting = {
                            'moderate': {
                                'room': str,
                                'anything': bool,
                                'spam': bool,
                                'banword': bool,
                                'caps': bool,
                                'stretching': bool,
                                'groupchats': bool,
                                'urls': bool
                            },
                            'broadcastrank': ' ',
                            'allowgames': False,
                            'tourwhitelist': []
                        }
        users: map, maps user ids to users.
        rank: string, the rank of this bot in this room.
        loaded: bool, determines if all the information for this room has been loaded yet.
        broadcastrank: string, rank required in this room for users to use commands.
    """
    def __init__(self, name, room_setting=None):
        """Intializes room with preliminary information."""
        if not room_setting:
            room_setting = {
                'moderate': {
                    'room': name.lower(),
                    'anything': False,
                    'spam': False,
                    'banword': False,
                    'caps': False,
                    'stretching': False,
                    'groupchats': False,
                    'urls': False
                },
                'broadcastrank': ' ',
                'allow games': False,
                'tourwhitelist': []}
        self.users = {}
        self.rank = ' ' # should be changed later
        self.name = name.lower()
        self.room_setting = room_setting
        self.loaded = False
        self.is_pm = self.name == 'pm'
        self.broadcastrank = self.room_setting['broadcastrank']

    def add_user(self, user):
        """Adds a user to the current rooms list of users.
        Args:
            user: User object, user object containing rank, userid, name, etc.
        """
        if user.id not in self.users:
            self.users[user.id] = user


