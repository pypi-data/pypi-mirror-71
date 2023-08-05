from typing import (
    Pattern,
    Tuple,
    Sequence,
    Set,
    Mapping,
    Hashable,
    Union,
    Optional,
)
import discord

__all__ = [
    "Roles",
    "RolesMetaClass",
    "Permissions",
    "PermissionsMetaClass",
    "Members",
    "MembersSet",
]


class RolesMetaClass(type):
    """For roles without guild_id. ``Roles[x] <==> Roles(None)[x]``
    
    this is useful for authorize some specific roles irrespective of server
    
    Example::
    
        # To authorize Admin roles in all servers
        # roles = ('Admin',) and guild_id = None
        Fn.auth = Roles['Admin']
    """

    def __getitem__(cls, roles: Union[Tuple[Union[str, int]], Union[str, int]]):
        if type(roles) is not tuple:
            roles = (roles,)
        if slice in map(type, roles):
            raise TypeError("'slice' object is not allowded")
        return Roles(None, roles)


class Roles(metaclass=RolesMetaClass):
    """To group members with their roles in a server.
    
    This can't be used to Authorize in DM channel.
    
    Example::
    
        server1 = Roles(1234567890) # guild_id of server1
        Fn.auth = {server1['Admin','Mod'], Roles[0987654321]}
        # authorizes:
        #    members with both 'Admin' and 'Mod' roles in server1
        #    members with role.id 0987654321
    """

    def __init__(
        self, guild_id: Optional[int] = None, roles: Optional[Tuple[Union[str, int]]] = None
    ):
        self.guild_id = guild_id
        self.roles = ("@everyone",) if roles is None else roles

    def __getitem__(self, roles: Union[Tuple[Union[str, int]], Union[str, int]]):
        if type(roles) is not tuple:
            roles = (roles,)
        if slice in map(type, roles):
            raise TypeError("'slice' object is not allowded")
        return Roles(self.guild_id, roles)

    def __repr__(self):
        return "<Roles guild_id={0} roles={1}>".format(self.guild_id, self.roles)

    def __str__(self):
        return str((self.guild_id, *self.roles))


class PermissionsMetaClass(type):
    """For permissions without guild_id. ``Permissions[x] <==> Permissions(None)[x]``
    
    this is useful for check some permissions irrespective of server
    
    Example::
    
        # To authorize members with Administrator permission in all servers
        # discord.permissions.Permissions(administrator=True) and guild_id = None
        Fn.auth = Permissions['administrator']
    """

    def __getitem__(cls, permissions: Union[Tuple[Union[str, int]], Union[str, int]]):
        if type(permissions) is not tuple:
            permissions = (permissions,)
        if slice in map(type, permissions):
            raise TypeError("'slice' object is not allowded")

        kwargs = dict()
        for key in permissions:
            if type(key) is int:
                kwargs["permissions"] = key
            elif key.startswith("!"):
                kwargs[key[1:]] = False
            else:
                kwargs[key] = True
        return Permissions(None, **kwargs)


class Permissions(discord.permissions.Permissions, metaclass=PermissionsMetaClass):
    """To group members with their permissions in a server.
    
    This can't be used to Authorize in DM channel.
    
    Example::
    
        server1 = Permissions(1234567890) # guild_id of server1
        Fn.auth = {server1['manage_guild', 'manage_roles'],
                   Permissions(0987654321, administrator=True)}
        # authorizes:
        #    members with both ManageServer and ManageRoles permissions in server1
        #    members with Administrator permission in server with guild_id 0987654321
    """

    def __init__(self, guild_id: Optional[int] = None, permissions: int = 0, **kwargs: bool):
        self.guild_id = guild_id
        super().__init__(permissions=permissions, **kwargs)

    def __getitem__(self, permissions: Union[Tuple[Union[str, int]], Union[str, int]]):
        if type(permissions) is not tuple:
            permissions = (permissions,)
        if slice in map(type, permissions):
            raise TypeError("'slice' object is not allowded")

        kwargs = dict()
        for key in permissions:
            if type(key) is int:
                kwargs["permissions"] = key
            elif key.startswith("!"):
                kwargs[key[1:]] = False
            else:
                kwargs[key] = True
        return Permissions(self.guild_id, **kwargs)

    def __repr__(self):
        return "<Permissions guild_id={0} value={1}>".format(self.guild_id, self.value)

    def __str__(self):
        return str((self.guild_id, self.value))


MemberIdentity = Union[int, str, Pattern, Roles, Permissions]
MemberGroups = Union[Sequence[Set[MemberIdentity]], Mapping[Hashable, Set[MemberIdentity]]]


class Members:
    """To group members for authorization
    
    Example::
    
        level = Members([{'root#0000','admin#1000'}, {'user1#1001'}])
        def privileged_cmd(msg, *args):
            #code#
        privileged_cmd.auth = level[0]
    """

    def __init__(self, groups: MemberGroups):
        """
        Args:
            groups : Sequence or Mapping of Set of MemberIdentity
        """

        self.groups = groups

    # subscript
    def __getitem__(self, arg: Hashable):
        """MemberGroups => MemberGroup
        """
        return MembersSet(self, ("__getitem__", arg))

    # Union
    def __or__(self, arg: Union["Members", "MembersSet", Set[MemberIdentity]]):
        if type(arg) is set:
            arg = set(arg)
        return MembersSet(self, ("__or__", arg))

    # Intersection
    def __and__(self, arg: Union["Members", "MembersSet", Set[MemberIdentity]]):
        if type(arg) is set:
            arg = set(arg)
        return MembersSet(self, ("__and__", arg))

    # Difference
    def __sub__(self, arg: Union["Members", "MembersSet", Set[MemberIdentity]]):
        if type(arg) is set:
            arg = set(arg)
        return MembersSet(self, ("__sub__", arg))

    # Symmetric difference
    def __xor__(self, arg: Union["Members", "MembersSet", Set[MemberIdentity]]):
        if type(arg) is set:
            arg = set(arg)
        return MembersSet(self, ("__xor__", arg))

    @property
    def members(self) -> Set[MemberIdentity]:
        """To return all the members
        """
        return MembersSet(self).members

    def __repr__(self):
        return "MemberGroups(" + repr(self.groups) + ")"

    def __str__(self):
        return str(self.groups)


class MembersSet:
    """Set of members subscripted from Members.
    
    It is alos possible to do set operations.
    
    Example::
    
        group = Members({'Admin': {'admin1#0001', 'admin2#0002'},
                         'users': {'user1#1001', 1234567890}})
        def privileged_cmd(msg, *args):
            #code#
        privileged_cmd.auth = group['Admin']|{'root#0000'}
        def cmd(msg, *args):
            #code#
        cmd.auth = group # <==> group['Admin']|group['users']
    """

    def __init__(self, Groups: Members, *MethodCalls):
        """
        Args:
            MemberGroups : Members instance for groups
            MethodCalls  : previous method calls
        """

        self.Groups = Groups
        self.chain = list(MethodCalls)

    # Union
    def __or__(self, arg: Union[Members, "MembersSet", Set[MemberIdentity]]):
        if type(arg) is set:
            arg = set(arg)
        return MembersSet(self.Groups, *self.chain, ("__or__", arg))

    # Intersection
    def __and__(self, arg: Union[Members, "MembersSet", Set[MemberIdentity]]):
        if type(arg) is set:
            arg = set(arg)
        return MembersSet(self.Groups, *self.chain, ("__and__", arg))

    # Difference
    def __sub__(self, arg: Union[Members, "MembersSet", Set[MemberIdentity]]):
        if type(arg) is set:
            arg = set(arg)
        return MembersSet(self.Groups, *self.chain, ("__sub__", arg))

    # Symmetric difference
    def __xor__(self, arg: Union[Members, "MembersSet", Set[MemberIdentity]]):
        if type(arg) is set:
            arg = set(arg)
        return MembersSet(self.Groups, *self.chain, ("__xor__", arg))

    @property
    def members(self) -> Set[MemberIdentity]:
        """members set with all operations done.
        
        All the operations done to :obj:`Members` is only executed 
        at the time of ``getattr(MembersObj, "members")``
        
        So, no need to update auth of each callbacks
        after updating the group.
        
        Example::
        
            group = Members([{'root#0000'}])
            Admin = group[0]|{'admin1#0001'}
            print(Admin.members) #{'root#0000', 'admin1#0001'}
            group.Groups[0] = {'admin2#0002'}
            print(Admin.members) #{'admin1#0001', 'admin2#0002'}
        """

        if len(self.chain) == 0:
            membersSet = set()
            if isinstance(self.Groups.groups, Sequence):
                for members_ in self.Groups.groups:
                    membersSet |= members_
            elif isinstance(self.Groups.groups, Mapping):
                for members_ in self.Groups.groups.values():
                    membersSet |= members_
            return membersSet

        method = self.chain[0][0]
        arg = self.chain[0][1]
        if method == "__getitem__":
            membersSet_ = getattr(self.Groups.groups, method)(arg)
            if type(membersSet_) is not set:  # for slicing
                membersSet = set()
                for members_ in membersSet_:
                    membersSet |= set(members_)
            else:
                membersSet = set(membersSet_)
        else:
            membersSet = self.Groups.members
            if type(arg) is MembersSet or type(arg) is Members:
                arg = arg.members
            membersSet = getattr(membersSet, method)(arg)

        if len(self.chain) == 1:
            return membersSet

        for call in self.chain[1:]:
            method = call[0]
            arg = call[1]
            if type(arg) is MembersSet or type(arg) is Members:
                arg = arg.members
            membersSet = getattr(membersSet, method)(arg)

        return membersSet

    def __repr__(self):
        return "Members(" + repr(self.members) + ")"

    def __str__(self):
        return str(self.members)
