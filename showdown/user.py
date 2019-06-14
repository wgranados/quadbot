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
import re


class UnSpecifiedUserRankException(Exception):
    """This error is thrown in the case that there is a new user added by the
    admins of PokemonShowdown, i.e. when they added the new bot user rank.
    """
    def __init__(self, user_class):
        self.user_class = user_class

    def __str__(self):
        return 'Unsupported user class:' + self.user_class


class User:
    """ Container class for basic user information collected from rooms.

    This information consists of user.id, user.rank, and user.name. user.id is
    a format-removed id of user.name with only a-z lowercase and 0-9 present.

    user.rank contain the auth level of the user, as a single character string of
    either ' ', +, ☆, %, @, *, &, #, or ~. Note that ☆ is only relevant for
    battle rooms.

    To compare groups against each other User.Groups have the information required
    when used like: User.Groups[user.rank] for a numeric value.

    Lastly, user.name is the unaltered name as seen in the chat rooms, and can be
    used for things like replying. Comparison between users should make use of
    user.id since users can change their frequently.

    Attributes:
        Groups: map string to int, ranks precedence of user ranks by symbols.
        name: string, username.
        id: string, simplified unique username.
        rank: string, user rank.
        owner: Bool, is this you.
    """
    Groups = {' ': 0, '+': 1, '☆': 1, '%': 2, '@': 3, '*': 4, '&': 5, '#': 6, '~': 7}

    def __init__(self, name, rank=' ', owner=False):
        self.name = name
        self.id = User.username_to_id(self.name)
        self.rank = rank
        self.owner = owner

    @staticmethod
    def username_to_id(name):
        return re.sub(r'[^a-zA-z0-9]', '', name).lower()

    @staticmethod
    def compare_ranks(rank1, rank2):
        """Compares two user ranks.
        Args:
            rank1: char, user rank of first person
            rank2: char, user rank of second person
        Returns:
            True if user rank 1 is greater than user rank 2
        Exception:
            UnSpecifiedUserClassException
        """
        try:
            return User.Groups[rank1] >= User.Groups[rank2]
        except KeyError:
            if rank1 not in User.Groups:
                raise UnSpecifiedUserRankException(rank1)
            if rank2 not in User.Groups:
                raise UnSpecifiedUserRankException(rank2)

    def is_owner(self):
        """Checks if the current user object is the master(hence you)"""
        return self.owner

    def has_rank(self, rank):
        """Determines if a user has sufficient staff rights"""
        return self.owner or User.compareRanks(self.rank, rank)
