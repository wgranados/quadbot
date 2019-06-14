import plugins.CommandAliases as CommandAliases


class DuplicateAliasConflict(Exception):
    pass


class UnreachableCommand(Exception):
    pass


class CommandBase(object):
    """Wrapper class for all commands written in this Bot.

    Defines main behaviour each command should have and also keeps track of
    duplicate commands.

    Attributes:
        aliases: list of str, keeps track of all the aliases that evoke this command
        can_learn: Bool,  specifying if chat data should be sent to this bot.
    """
    def __init__(self, aliases, can_learn):
        if not aliases:
            raise UnreachableCommand
        # check for conflicts and raise exception if found
        for alias in aliases:
            if CommandAliases.conflict(alias):
                raise DuplicateAliasConflict
            else:
                CommandAliases.add_alias(alias)
        self.aliases = aliases
        self.can_learn = can_learn

    def parse_args(self, msg):
        """Default parsing for commands by commas.
        Args:
            msg: str, string containing information from user.
        Returns:
            list of str, containing arguments pass to command
        """
        return list(filter(lambda m: m != '', [item.strip() for item in msg.split(',')]))


    def learn(self, room, user, data):
        """ Use user chat data to modify command behaviour.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            data: str, messages recorded by user in chat.

        Returns:
            None
        """
        raise NotImplementedError

    def response(self, room, user, args):
        """ Returns a response to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        raise NotImplementedError

    def _help(self, room, user, args):
        """ Returns a help response to the user.

        In particular gives more information about this command to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        raise NotImplementedError

    def _error(self, room, user, reason):
        """ Returns an error response to the user.

        In particular gives a helpful error response to the user. Errors can range
        from internal errors to user input errors.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            reason: str, reason for this error.
        Returns:
            ReplyObject
        """
        raise NotImplementedError

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
        raise NotImplementedError
