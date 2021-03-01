
from typing import Union

from discord import Reaction, User, Member
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.context import Context

from config import config
from src import Database
from src.attendance.enums import Locations
from src.attendance import AttendanceRequest
from src.utils import Emoji, mention_to_id


class AttendanceCog(commands.Cog):

    def __init__(self, bot: Bot, database: Database):

        self.bot = bot
        self.db = database

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
            self.db.update({'_id': mention}, becode_token=token)
            await context.send(f"{mention}, your token has been added")

        else:
            await context.send(f"{mention}, your token is not valid")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: Union[User, Member]):
        """Event triggered when a user click a reaction to send an attendance to Becode."""

        # Get all attendance message posted
        messages = config.ATTENDANCE_MESSAGES.get_by_messages()

        # Check when a user add a reaction
        if reaction.message.id in messages.keys() and not user.bot:
            location = None

            # Emoji: House
            if str(reaction.emoji == Emoji.HOUSE.value):
                location = Locations.HOME

            # Emoji: City
            elif str(reaction.emoji == Emoji.CITY.value):
                location = Locations.BECODE

            if location:
                print("[!] User added reaction.")

                # Get the mention
                mention: str = user.mention

                # Retrieve the token and check if it's not None
                if token := self.db.get_token(mention):

                    # Send an attendance request to Becode
                    if await AttendanceRequest(messages[reaction.message.id], location, token).send():

                        print(f"[!] Attendance was correctly send for {mention}.")
                        await user.send(f"{mention} J'ai bien pointé pour toi sur Becode !")

                    else:
                        print(f"[!] Attendance was NOT correctly send for {mention}.")
                        await user.send(f"{mention} OUPS ! Une **erreur** s'est produite... Passe par https://my.becode.org pour pointer.")

                else:
                    print(f"[!] Missing token for {mention}.")
                    await user.send(f"{mention} OUPS ! Une **erreur** s'est produite: Je n'ai pas trouvé ton token... Ajoute un token avec la commande **!token**.")
