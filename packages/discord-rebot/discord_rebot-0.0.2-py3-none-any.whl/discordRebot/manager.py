import inspect
import textwrap
from typing import (
    NewType,
    MutableMapping,
    Callable,
    Protocol,
    Pattern,
    Sequence,
    Set,
    Mapping,
    Union,
    Optional,
)
import re
import discord

from .members import *

__all__ = ["Manager", "Mapper", "Authorize", "AuthorizeCallBack", "RE_MARKDOWN", "ZWS"]

PatternVstr = Union[Pattern, str]
MemberIdentity = Union[int, str, Pattern, Roles, Permissions]
Message = NewType("Message", discord.Message)
Author = NewType("Author", discord.Message.author)
Auth = Union[
    Members,
    MembersSet,
    MemberIdentity,
    Set[MemberIdentity],
    Sequence[MemberIdentity],
    Callable[[Author], bool],
]


def Authorize(members: Auth, message: Message) -> Union[MemberIdentity, None]:
    """Authorize whether member belongs to members
    
    Args:
        members : authorized members
        message : message.author to be authorized
    
    Returns:
        memberIdentity used for authorization
        or None if not authorized *(member not belongs to members)*
    """

    member: Author = message.author

    if type(members) is MembersSet or type(members) is Members:
        members = members.members
    elif (
        type(members) is int
        or type(members) is str
        or type(members) is Roles
        or type(members) is Permissions
        or isinstance(members, Pattern)
        or isinstance(members, Callable)
    ):
        members = {members}
    for memberIdentity in members:
        if type(memberIdentity) is int:
            if member.id == memberIdentity:
                return memberIdentity

        elif type(memberIdentity) is str:
            if str(member) == memberIdentity:
                return memberIdentity

        elif type(memberIdentity) is Roles:
            # DMchannel don't have roles
            if not hasattr(member, "roles"):
                continue
            if memberIdentity.guild_id:
                guild_id = memberIdentity.guild_id
                if guild_id != member.guild.id:
                    continue

            required_roles = memberIdentity.roles
            member_roles_id = [role.id for role in member.roles]
            member_roles_name = [role.name for role in member.roles]
            for role in required_roles:
                if type(role) is int:
                    if role not in member_roles_id:
                        break
                elif type(role) is str:
                    if role not in member_roles_name:
                        break
            else:
                return memberIdentity

        elif type(memberIdentity) is Permissions:
            # DMchannel don't have permissions
            if not hasattr(member, "guild_permissions"):
                continue
            if memberIdentity.guild_id:
                guild_id = memberIdentity.guild_id
                if guild_id != member.guild.id:
                    continue

            if getattr(member, "guild_permissions") >= memberIdentity:
                return memberIdentity

        elif isinstance(memberIdentity, Pattern):
            if memberIdentity.match(str(member)):
                "str(message.author) -> 'user_name#user_discriminator'"
                return memberIdentity

        else:
            if memberIdentity(message):
                return memberIdentity

    return None


# fmt: off
class CallBack(Protocol):
    def __call__(self, msg: Message, /, *args: str) -> Optional[str]: ...
    auth: Optional[Auth] = None
    has_roles: Optional[Union[Roles, Set[Roles], Sequence[Roles]]] = None
    has_permissions: Optional[Union[Permissions, Set[Permissions], Sequence[Permissions]]] = None
# fmt: on


def AuthorizeCallBack(callback: CallBack, message: Message) -> bool:
    """Checks whether member is authorized to access the callback
    
    Args:
        callback : callback for which authorizing member
        message  : message.author to be authorized
    
    Returns:
        True if authorized else False
    """

    if hasattr(callback, "auth"):
        auth = getattr(callback, "auth")
        if auth:
            if not Authorize(auth, message):
                return False

    if hasattr(callback, "has_roles"):
        has_roles = getattr(callback, "has_roles")
        if has_roles:
            if not Authorize(has_roles, message):
                return False

    if hasattr(callback, "has_permissions"):
        has_permissions = getattr(callback, "has_permissions")
        if has_permissions:
            if not Authorize(has_permissions, message):
                return False

    return True


class Mapper:
    """To create P2F map easily using decorator
    
    Example::
    
        key = Mapper()
        @key(re.compile(r'^! ([\\s\\S]*)$'))
        def cmd1(msg, arg):
            #code#
        @key('cmd2','command2') # 'command2' and 'cmd2' both mapped to cmd2 callback
        def cmd2(msg):
            #code#
        client.event(Manager(key).on_message)
    """

    def __init__(self, P2F: Optional[MutableMapping[PatternVstr, CallBack]] = None):
        """
        Args:
            P2F : dict if you want to continue with previous P2F
                or None to create new one
        """

        self.P2F = dict() if P2F is None else P2F

    def __call__(self, *match_with: PatternVstr) -> Callable[[CallBack], CallBack]:
        """For mapping decorated function
        """

        def updateP2F(callback: CallBack) -> CallBack:
            for key in match_with:  # for multiple commands to a callback
                self.P2F[key] = callback
            return callback

        return updateP2F  # decorator

    def __getattr__(self, attribute):
        return getattr(self.P2F, attribute)

    def __getitem__(self, key):
        return self.P2F.__getitem__(key)

    def __repr__(self):
        return "Mapper(" + repr(self.P2F) + ")"

    def __str__(self):
        return str(self.P2F)


RE_MARKDOWN = re.compile(r"([*_~`|>])")
ZWS = "\u200B"  # Unicode Character 'ZERO WIDTH SPACE' (U+200B)


class Manager:
    """To manage all commands with their respective authorized authors
    """

    ContentFieldLimits = 2000

    def __init__(
        self,
        P2F: Union[Mapping[PatternVstr, CallBack], Mapper] = {
            re.compile(r"^!echo (.*)$"): lambda msg, x: x
        },
        authorize: bool = True,
        escMD: bool = False,
        listenBot: bool = False,
        filter: Optional[Callable[[Message], bool]] = None,
    ):
        """
        Args:
            P2F : Pattern or Str to Function *(callback)* Map (or) :class:`Mapper` object
            
                | if Pattern matchs with message.content 
                  then callback is called with message, captured groups
                | if Str is equal to message.content then callback is called with message
                | In both the return string by callback is the reply message.
                  No reply if return value is None.
            
            authorize : allow only Authorized members to execute command *(to call callback)*
            
                | if False all callbacks *(P2F.values())* is callable by all members
                | else for each command only members authorized
                  by :func:`AuthorizeCallBack` is allowded.
            
            escMD : escape MarkDown while reply
            
                | if true reply *(returned by callback)* is filtered to escape MarkDown
                | else no filtering to escape MarkDown.
            
            listenBot : allow reply to bot's message (this may leads to infinte loop of messages)
            
                | if true bot's message can't be skiped in on_message
            
            filter : function to filter messages
            
                | if filter(message) is True then proceed on_message
                | else skip that message and continue
        """

        self.P2F = P2F
        self.authorize = authorize
        self.escMD = escMD
        self.listenBot = listenBot
        self.filter = filter

    async def on_message(self, message: Message):
        """It is the on_message event listner.
        
        set it in **client.event** like ``client.event(Manager().on_message)``
        """

        if self.filter:
            if not self.filter(message):
                return

        # Don't reply to bot's reply if listenBot disabled
        if not self.listenBot and message.author.bot:
            return

        for cmd, callback in self.P2F.items():
            if type(cmd) is str:
                if cmd == message.content:
                    await self.execute(callback, message)
            else:
                match = cmd.match(message.content)
                if match:
                    await self.execute(callback, message, *match.groups())

    async def execute(self, callback: CallBack, message: Message, *args: str):
        """To execute the matched function, if the author is authorized 
        by :func:`AuthorizeCallBack`
        
        Example::
        
            def cmd(msg, *args):
                #code#
            cmd.auth = None
        
        Args:
            callback   : function to be called if message.author is Authorized
                         by :func:`discordRebot.manager.AuthorizeCallBack`
            message    : message object from discord, having all details about a message
            *args (str): arguments to pass into callback
        """

        if self.authorize:
            if not AuthorizeCallBack(callback, message):
                denial_message = await self.on_denied(callback, message)
                await self.reply(message, denial_message)
                return

        if inspect.iscoroutinefunction(callback):
            response = await callback(message, *args)
            await self.reply(message, response)

        elif inspect.isasyncgenfunction(callback):
            async for response in callback(message, *args):
                await self.reply(message, response)

        elif inspect.isgeneratorfunction(callback):
            for response in callback(message, *args):
                await self.reply(message, response)

        else:
            response = callback(message, *args)
            await self.reply(message, response)

    async def reply(self, message: Message, response: Union[str, None]):
        """To send the response from callback in :meth:`execute`
        
        Args:
            message  : message object from discord, having all details about a message
            response : response from callback
        """

        if not response:
            return
        elif type(response) is not str:
            response = str(response)

        if self.escMD:
            response = RE_MARKDOWN.sub(r"\\\1", response)

        if len(response) > self.ContentFieldLimits:
            for response in textwrap.wrap(response, self.ContentFieldLimits):
                await message.channel.send(response)
        else:
            await message.channel.send(response)

    async def on_denied(self, callback: CallBack, message: Message) -> Optional[str]:
        """Called when unauthorized and returns the denial message
        
        Args:
            callback : command which is skiped due to unauthorized
            message  : message object from discord, having all details about a message
        Returns:
            denial message
        """
        return ":{ Not Permitted"


# The above Type Hints are not for type checking
# Don't do mypy since this code is more dynamic and duck-type
