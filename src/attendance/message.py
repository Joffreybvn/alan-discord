
from datetime import datetime
from typing import Tuple
from pytz import timezone
from typing import Union

from discord import Client, TextChannel, DMChannel, User, Embed, Message, PartialMessage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import config
from src.database import Database
from src.utils import Emoji, mention_to_id
from src.attendance.enums import Periods

# Create the scheduler and set the timezone.
scheduler = AsyncIOScheduler()
tz = timezone('Europe/Brussels')


class AttendanceMessage:

    def __init__(self, client: Client, database: Database, period: Periods,
                 display_time: tuple, hide_time: tuple, display_days: str = "mon, tue, wed, thu, fri"):

        # Discord client
        self.client = client
        self.database = database

        # Schedule values
        self.time: str = period.value
        self.days: str = display_days
        self.display_time: Tuple[int, int] = display_time
        self.hide_time: Tuple[int, int] = hide_time

        # Message text
        self.text = "C'est le moment de **pointer** sur My BeCode !"

        # Schedule the message
        self.schedule()

    @staticmethod
    def get_embed() -> Embed:

        embed = Embed(
            title="My BeCode",

            description=f"""
            In Attendance We Trust ! Pointez maintenant sur [my.becode.org]({config.MY_BECODE_URL}).
            Ou cliquez directement sur l'une des réactions ci-dessous.""",

            url=config.MY_BECODE_URL,
            colour=5747135
        )
        embed.set_thumbnail(url="https://i.imgur.com/ixU2HdV.gif")  # https://i.imgur.com/cg4xd66.png

        return embed

    async def __send_attendance_message(self, context: Union[TextChannel, User]) -> Message:
        """
        Send an attendance message into a TextChannel or in Direct Message
        to a user, and append the reactions. Return the id of the send message.
        """

        # Send the message
        message: Message = await context.send(self.text, embed=self.get_embed())

        # Append the reactions
        await message.add_reaction(emoji=Emoji.HOUSE.value)
        await message.add_reaction(emoji=Emoji.CITY.value)

        # Return the message
        return message

    def schedule(self):

        # Display
        display_hour, display_minute = self.display_time

        @scheduler.scheduled_job('cron', day_of_week=self.days, hour=display_hour, minute=display_minute, timezone=tz)
        async def display():
            nonlocal self

            for channel_id in config.CHANNEL_ATTENDANCE:
                channel: TextChannel = self.client.get_channel(channel_id)

                # Send the message with reactions
                message: Message = await self.__send_attendance_message(channel)

                # Save the message to later detect clicks ont reactions
                config.ATTENDANCE_MESSAGES.add(self.time, channel_id, message.id)

            # Log: job triggered
            print(f"[i] Display server attendance - Triggered @ {datetime.now()}")

            for user_id in self.database.get_pingable_users():
                user: User = await self.client.fetch_user(mention_to_id(user_id))

                # Send the message with reactions
                message: Message = await self.__send_attendance_message(user)
                channel: DMChannel = message.channel

                # Save the message to later detect clicks ont reactions
                config.ATTENDANCE_MESSAGES.add(self.time, channel.id, message.id)

            # Log: job triggered
            print(f"[i] Display direct message attendance - Triggered @ {datetime.now()}")

        # Hide
        hide_hour, hide_minute = self.hide_time

        @scheduler.scheduled_job('cron', day_of_week=self.days, hour=hide_hour, minute=hide_minute, timezone=tz)
        async def hide():
            nonlocal self

            # Get each channel and message to delete, and delete them
            for channel_id, message_id in config.ATTENDANCE_MESSAGES.get(self.time).items():

                channel: Union[TextChannel, DMChannel] = self.client.get_channel(channel_id)
                message: PartialMessage = channel.get_partial_message(message_id)
                await message.delete()

            # Clean the attendance message dict
            config.ATTENDANCE_MESSAGES.empty(self.time)

        # Job registered
        print(f"[+] Attendance jobs scheduled: {self.days} @ {display_hour}h{display_minute}")

    @staticmethod
    def start():
        """Start all schedulers."""

        scheduler.start()
