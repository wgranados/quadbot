
from showdown.user import User


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


