
from discord import User, RawReactionActionEvent, PartialEmoji
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.context import Context

from config import config
from src.database import Database
from src.attendance.enums import Locations
from src.attendance import AttendanceRequest
from src.utils import Emoji


class AttendanceCog(commands.Cog):

    def __init__(self, bot: Bot, database: Database):

        self.bot: Bot = bot
        self.db: Database = database

    @commands.command(name="token", pass_context=True)
    async def add_token(self, context: Context, token: str):
        """Add the the given token to the database."""

        # Save the action to the history
        self.bot.history[context.message.id] = True

        # Get the author
        mention: str = context.message.author.mention

        # Check if the token is provided
        if len(token) > 1:

            # Update the database
            self.db.upsert_user(user_id=mention, becode_token=token)
            await context.send(f"{mention}, your token has been added")

        else:
            await context.send(f"{mention}, your token is not valid")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """Event triggered when a user click a reaction to send an attendance to Becode."""

        # Get the user object
        user: User = await self.bot.fetch_user(payload.user_id)

        # If the reaction is added by a human
        if not user.bot:

            # Get all attendance message posted
            messages = config.ATTENDANCE_MESSAGES.get_by_messages()

            # Get the emoji and message id
            emoji: PartialEmoji = payload.emoji
            message_id: int = payload.message_id

            # Check when a user add a reaction
            if message_id in messages.keys():
                location = None

                # Emoji: House
                if str(emoji == Emoji.HOUSE.value):
                    location = Locations.HOME

                # Emoji: City
                elif str(emoji == Emoji.CITY.value):
                    location = Locations.BECODE

                if location:
                    print("[!] User added reaction.")

                    # Get the mention
                    mention: str = user.mention

                    # Retrieve the token and check if it's not None
                    if token := self.db.get_token(mention):

                        # Send an attendance request to Becode
                        status, message = await AttendanceRequest(messages[message_id], location, token).send()
                        if status:

                            print(f"[!] Attendance was correctly send for {mention}.")
                            await user.send(f"{mention} J'ai bien pointé pour toi sur Becode !")

                        else:
                            print(f"[!] Attendance was NOT correctly send for {mention}.")
                            await user.send(f"{mention} OUPS ! Une **erreur** s'est produite: Ton token est probablement expiré. Passe par https://my.becode.org pour pointer.")

                            if message:
                                await user.send(str(message))

                    else:
                        print(f"[!] Missing token for {mention}.")
                        await user.send(f"{mention} OUPS ! Une **erreur** s'est produite: Je n'ai pas trouvé ton token... Ajoute un token avec la commande **!token**.")