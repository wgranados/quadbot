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

from urllib.request import urlopen
from io import BytesIO
from PIL import Image


class OnlineImage(object):
    """Gets basic atribute for online images like dimensions) """
    @staticmethod
    def get_image_info(URL):
        """ Gets the the content type, width, and height of the repective image
        Args:
            URL: str, link to the image i.e.  'http://imgs.xkcd.com/comics/wifi.png'
        Returns:
            tuple of (int:width, int:height)
        """
        file = BytesIO(urlopen(URL).read())
        im = Image.open(file)
        width, height = im.size
        return width, height

    @staticmethod
    def get_local_image_info(file_name):
        """ Gets the the content type, width, and height of the respective image
        Args:
            file_name: str, link to the image i.e.  'default.png'
        Returns:
            tuple of (str:content_type, int:width, int:height)
        """
        with Image.open(file_name) as im:
            width, height = im.size
            return width, height
