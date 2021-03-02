
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.context import Context

from config import config
from src.database import Database


class AdministrationCog(commands.Cog):
    """
    These Cogs can we used only by users defined as "Operator" in
    the environment variables.
    """

    def __init__(self, bot: Bot, database: Database):
        self.bot: Bot = bot
        self.db: Database = database

    @commands.command(name="addchannel", pass_context=True)
    async def add_channel(self, context: Context, channel_type: str, channel_id: int):

        # Check the channel type is correct
        if channel_type in config.CHANNEL_TYPES:
            self.db.add_channel(channel_type, channel_id)

    @commands.command(name="removechannel", pass_context=True)
    async def remove_channel(self, context: Context, channel_type: str, channel_id: int):

        # Check the channel type is correct
        if channel_type in config.CHANNEL_TYPES:
            self.db.remove_channel(channel_type, channel_id)
