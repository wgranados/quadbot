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
    def __str__(self):
        return 'name: {}, userid: {}, rank: {}'.format(self.name, self.id, self.rank)
