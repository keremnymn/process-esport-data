class TeamsLengthError(Exception):
    """
    Raises when the length of teams is not 2
    """

    pass


class PlayersLengthError(Exception):
    """
    Raises when the length of players is not 5
    """

    pass


class InvalidEventType(Exception):
    """
    Raises when the event type is not valid
    """

    pass


class InvalidPlayerID(Exception):
    """
    Raises when the player ID is not valid
    """

    pass


class InvalidTeamID(Exception):
    """
    Raises when the team ID is not valid
    """

    pass
