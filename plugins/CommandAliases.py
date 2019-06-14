global_aliases = {}


def conflict(command_aliases):
    """Determines if there are conflicting commands

    Args:
        command_aliases: list of str, aliases for this command
    Returns:
        True if there is a conflict, false otherwise
    """
    for alias in command_aliases:
        if alias in global_aliases:
            return True
    return False


def add_alias(alias):
    """Add alias to global aliases"""
    global_aliases[alias] = True
