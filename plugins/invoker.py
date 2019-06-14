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

import asyncio
import importlib
import glob
from showdown import ReplyObject

class Invoker:
    """Invoker class for handling dynamic loading of command classes.

    In order for a command to be dynamically loaded on start, it should adhere
    to the following: the name of class file must end in Command.py (for example
    CreditsCommand.py), a class must be instantiated inside it with the same
    Prefix (for example for CreditsCommands.py, there must be a class definition
    for Credits), and the class must implement the behaviour of a CommandBase.
    
    Attributes:
        modules: list of CommandBase, commands which implement the CommandBase 
                 behaviours.
    """
    def __init__(self):
        self.modules = []
        self._load_modules()

    def _load_modules(self):
        """Loads in command files labelled as *Command.py in plugins folder."""
        module_paths = self.get_files('plugins')
        print('Loading command modules.')
        for path in module_paths:
            base_file_path = path.replace('/', '.')[:-3]
            class_name = base_file_path[base_file_path.rfind('.')+1 : base_file_path.rfind('Command')]
            class_var = getattr(importlib.import_module(base_file_path), class_name)
            obj = class_var()
            self.modules.append(obj)
            print('{} has been loaded.'.format(class_var.__name__))
            print(base_file_path, class_name)
            print('\n')


    def get_files(self, master_path):
        """Recursively gets the path to all html files in a directory.

	Essentially master_path will be one of the following cases:
	1) '', an empty string. In this case we just traverse the current
	   directory.
	2) 'index.h', a file with an non-html extension. In this case we have
	been directed to an unnessary file so we ignore it.
	3) 'folder/', the sub-directory of this folder. In this case we return
	   we just proceed as usual.
	4) 'folder', just a folder. In this case we just proceed as usual.

	Args:
	    master_path: str, the parent directory of the folder you wish to get
			 files from recursively. Leave empty if you want to
			 traverse the current directory.
	Raises:
	    None.
	Returns:
	    list of str, where each string is a path to a file.
	"""
        path = ''
        if not master_path or master_path == '':
            path = '*'
        elif master_path.endswith('/'):
            path = master_path + '*'
        else:
            path = master_path + '/*'
        items = glob.glob(path)
        ret = []
        for item in items:
            if item.endswith('Command.py'):
                ret.append(item)
            elif not item.endswith('Command.py'):
                sub_dir_ret = self.get_files(item)
                ret = ret + sub_dir_ret
        return ret

    def parse_alias(self, raw_message):
        """Retrieves the command invoked by the user.
        Args:
            raw_message: str, string message sent from the user.
        Returns:
            str, containing the command.
        """
        # parse the content from the command char '~' to the first white space
        first_white_space_index = raw_message.find(' ')
        alias = raw_message[1:] if first_white_space_index < 0 else raw_message[1:first_white_space_index]
        return alias

    @asyncio.coroutine
    def invoke_command(self, message):
        """Attempt to invoke invoke the specific command with provided arguments.
        Args:
            message: MessageWrapper, message wrapper containing content.
        Returns:
            
        """
        command_alias = self.parse_alias(message.content)
        command_msg = message.content[len(command_alias)+1:].lstrip()
        for cmd in self.modules:
            if command_alias in cmd.aliases:
                response = yield from cmd.response(message.room, message.user, cmd.parse_args(command_msg))
                return response
        return (yield from ReplyObject())

        
