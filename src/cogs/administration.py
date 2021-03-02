
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

        if context.author.id in config.OPERATORS:

            # Check if the channel type is correct
            if channel_type in config.CHANNEL_TYPES:

                # Check if the channel is correct
                if self.bot.get_channel(channel_id):

                    # Append the channel
                    self.db.add_channel(channel_type, channel_id)
                    await context.send(f"The channel was correctly added.")

                else:
                    await context.send(f"Incorrect channel id.")

            else:
                await context.send(f"Incorrect channel type. Available types: {config.CHANNEL_TYPES}")

    @commands.command(name="removechannel", pass_context=True)
    async def remove_channel(self, context: Context, channel_type: str, channel_id: int):

        if context.author.id in config.OPERATORS:

            # Check if the channel type is correct
            if channel_type in config.CHANNEL_TYPES:

                # Remove the channel
                self.db.remove_channel(channel_type, channel_id)
                await context.send(f"The channel was correctly removed.")

            else:
                await context.send(f"Incorrect channel type. Available types: {config.CHANNEL_TYPES}")
