from collections import defaultdict

from discord import DMChannel, Intents
from discord.ext import commands
from discord.message import Message
from botbuilder_discord import OfflineConnector

from src.database import Database
from .attendance.scheduler import Scheduler
from .cogs import NotificationCog, AttendanceCog, WatchCog, AdministrationCog
from config import Config

config = Config()
database = Database(config.DB_HOST, config.DB_PASSWORD)


# Doc: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html
class Bot(commands.Bot):

    def __init__(self):
        commands_prefixes = ['!']
        super().__init__(commands_prefixes)

        self.token = config.TOKEN
        self.history = defaultdict(lambda: False)

        # Start attendance scheduler
        self.scheduler = Scheduler(self, database)

        # Connect to NLU
        self.nlu = OfflineConnector(
            bot_api_url=config.BOT_API,
            listener_host=config.BOT_CALLBACK_HOST,
            listener_port=config.BOT_CALLBACK_PORT
        )

        # Register all Cogs
        self.add_cog(NotificationCog(self, database))
        self.add_cog(AttendanceCog(self, database))
        self.add_cog(WatchCog(self, database))
        self.add_cog(AdministrationCog(self, database))

    def run(self):
        """
        Override the run method to pass the token directly from self.token.
        """

        # Start the scheduler
        self.scheduler.start()

        # Connect the bot to Discord servers
        super(Bot, self).run(self.token)

    async def on_ready(self):
        """Triggered when the bot connects to Discord."""

        # Print a confirmation message to the console
        print(f'Bot connected to Discord with id: "{self.user}".')

    async def on_message(self, message: Message):
        """
        Triggered when a message is send on any channel/server that the
        bot have access.
        """

        # Consider message send only in whitelisted channels or in private message
        if type(message.channel) != DMChannel and message.channel.id not in config.CHANNEL_WHITELIST:
            return

        # Don't respond to ourselves
        if message.author == self.user:
            return

        # Don't respond to any bot
        if message.author.bot:
            return

        # Trigger the Cogs
        await super(Bot, self).on_message(message)

        # If the Cogs were not triggered, use NLP
        if not self.history[message.id]:
            if self.user.mentioned_in(message) or type(message.channel) == DMChannel:

                # Trigger the NLP
                responses = await self.nlu.send_message(message.author.id, message.content)

                # Send back its responses
                for response in responses:
                    await message.channel.send(response)

        else:
            del self.history[message.id]

