from plugins.CommandBase import CommandBase
from clients.pokemon.showdown import ReplyObject
from utils.details import config


class Broadcast(CommandBase):
    def __init__(self):
        super().__init__(aliases=['broadcast'], can_learn=False)

    def learn(self, room, user, data):
        pass

    async def response(self, room, user, args):
        """ Returns a response to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: no arguments should be passed except for help
        Returns:
            ReplyObject
        """
        if len(args) == 1 and args[0] == 'help':
            return self._help(room, user, args)
        elif len(args) >= 2:
            return ReplyObject("This command only takes 1 argument", True)
        elif len(args) == 1 and args[0] not in ['off', '+', '%', '@', '*', '#']:
            return ReplyObject("You have provided an invalid argument", True)
        elif len(args) == 1 and room.is_pm:
            return ReplyObject("There are no broadcast ranks in PMs", True)
        elif len(args) == 1 and not user.has_rank('#'):
            return ReplyObject("This command is reserved for Room Owners(#)", True)
        else:
            return self._success(room, user, args)

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
        if len(args) == 0:
            return ReplyObject('Rank required to broadcast: {rank}'.format(rank=room.broadcastrank))
        else:
            broadcast_rank = ' ' if args[0] == 'off' else args[0]
            room.broadcastrank = broadcast_rank
            return ReplyObject('Broadcast rank set to {rank}. (This is not saved on reboot)'.format(rank=broadcast_rank if not broadcast_rank == ' ' else 'none'), True)