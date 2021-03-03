
from datetime import datetime, timedelta
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.context import Context

from config import config
from src.database import Database
from src.utils import generate_uuid


class SettingsCog(commands.Cog):

    def __init__(self, bot: Bot, database: Database):

        self.bot = bot
        self.db = database

    @commands.command(name="settings", pass_context=True)
    async def get_settings_link(self, context: Context):

        # Save the action to the history
        self.bot.history[context.message.id] = True

        # Get the author
        mention: str = context.message.author.mention

        # Generate a UUID for the URL
        url_uuid: str = generate_uuid()

        # Append the token and their timeout to the database
        self.db.upsert_user(
            user_id=mention,

            # Set site token, valid up to 5 minutes
            site_token=url_uuid,
            site_token_timeout=datetime.now() + timedelta(minutes=2),

            # Set API access token, valid up to 24h
            access_token=generate_uuid(),
            access_token_timeout=datetime.now() + timedelta(hours=24)
        )

        # Send the url to the user
        await context.send(f"{mention} Use this one-time link to edit your settings: {config.TURINGBOT_URL}/#{url_uuid}")
