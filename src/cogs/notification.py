
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.context import Context

from src.database import Database


class NotificationCog(commands.Cog):

    def __init__(self, bot: Bot, database: Database):

        self.bot = bot
        self.db = database

    @commands.command(name="alert", pass_context=True)
    async def add_user_notification_list(self, context: Context):
        """
        Add the user to the notification list. He will then receive
        notifications for any scheduled messages send by the bot
        (attendances, pauses, meet, ...)
        """

        # Save the action to the history
        self.bot.history[context.message.id] = True

        # Update the database
        mention: str = context.message.author.mention
        self.db.upsert_user(user_id=mention, send_notification=True)

        # Send a confirmation to user
        await context.send(f"{mention} You will now receive notifications for attendances, meetings and breaks.")

    @commands.command(name="stopalert", pass_context=True)
    async def remove_user_notification_list(self, context: Context):
        """
        Remove the user from the notification list. He will no longer
        receive notifications from scheduled messages send by the bot
        (attendances, pauses, meet, ...)
        """

        # Save the action to the history
        self.bot.history[context.message.id] = True

        # Update the database
        mention: str = context.message.author.mention
        self.db.upsert_user(user_id=mention, send_notification=False)

        # Log and send a confirmation to user
        await context.send(f"{mention} You won't receive notifications anymore")
