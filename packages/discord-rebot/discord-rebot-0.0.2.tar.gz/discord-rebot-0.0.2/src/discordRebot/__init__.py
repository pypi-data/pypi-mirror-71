"""RegEx based command mapping discord BOT framework with authorization

discordRebot:
 | __init__.py
 | __main__.py
 | manager.py    # Main module
 | members.py    # has Roles, Permissions and Members classes
 | converter.py  # has Converter

__all__:
 | discord           : `discord`_
 | re                : `re`_
 | Manager           : :class:`discordRebot.manager.Manager`
 | Mapper            : :class:`discordRebot.manager.Mapper`
 | Converter         : :class:`discordRebot.converter.Converter`
 | Members           : :class:`discordRebot.members.Members`
 | Roles             : :class:`discordRebot.members.Roles`
 | Permissions       : :class:`discordRebot.members.Permissions`
 | Authorize         : :func:`discordRebot.manager.Authorize`
 | AuthorizeCallBack : :func:`discordRebot.manager.AuthorizeCallBack`
 | RE_MARKDOWN       : :obj:`re.Pattern` to escape MD
 | ZWS               : ``'\\u200B'``

Tested on:
 | python          v3.8.2-final
 | discord.py      v1.3.3-final
 | re              2.2.1

:Author: Naveen S R

:Maintainers:
 | Naveen S R (github: `nkpro2000sr <https://github.com/nkpro2000sr>`_)
 | srnaveen2k@yahoo.com
"""

__title__ = "discordRebot"
__author__ = "Naveen S R"
__license__ = "MIT"
__copyright__ = "Copyright 2020 Naveen S R"
__version__ = "0.0.2"

import re
import discord
from .manager import *
from .members import *
from .converter import *

__all__ = [
    "discord",  # just discord.py
    "re",  # just regex
    "Manager",  # class to manage all commands with a client
    "Mapper",  # to map all commands with its callback
    "Converter",  # to convert string to actual discord.* class objects
    "Members",  # to group members to Authorize for each commands
    "Roles",  # to group members based on their roles in servers
    "Permissions",  # to group members based on their permissions in servers
    "Authorize",  # function to check authorisation
    "AuthorizeCallBack",  # function to check authorisation for callback
    "RE_MARKDOWN",  # regex for markdown syntax in discord. substitute to escape MD
    "ZWS",  # just ZERO WIDTH SPACE character
]
