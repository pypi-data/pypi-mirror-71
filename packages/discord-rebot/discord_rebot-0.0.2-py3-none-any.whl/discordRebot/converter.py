import inspect
from typing import Any, NewType, Union
import discord
import discord.ext.commands as commands

__all__ = ["Converter"]

Message = NewType("Message", discord.Message)

dummy_parameter = inspect.Parameter("dummy", 0)
dummy_obj = object()


class Converter:
    """To convert *string* to actual **discord.\*** class objects
    
    Example::
    
        Convert = Converter(bot=client)
        member1 = await Convert(msg, 'nickname', discord.Member)
        assert isinstance(member1, discord.Member)
    
    client: :obj:`discord.Client` and msg: :obj:`discord.Message` is for lookup purpose
    """

    def __init__(self, bot: Union[discord.Client, commands.Bot]):
        """
        Args:
            bot : for creating ctx
        """

        self.bot = bot

    def _create_ctx(self, msg: Message):
        """To create ctx for passing into :func:`discord.ext.commands.Command._actual_conversion`
        
        Args:
            msg : for creating ctx
        
        Returns:
            ctx from msg and self.bot using :class:`discord.ext.commands.Context`
        """

        ctx = commands.Context(bot=self.bot, message=msg, prefix="dummy")
        return ctx

    async def __call__(self, msg: Message, from_: str, to: Any):
        """To convert
        
        Args:
            msg   : for :meth:`_create_ctx`
            from_ : from which we have to convert
            to    : to which we have to convert
        
        Returns:
            converted obj`to`
        """

        ctx = self._create_ctx(msg)

        converted = await commands.Command._actual_conversion(
            dummy_obj, ctx, to, from_, dummy_parameter
        )

        return converted
