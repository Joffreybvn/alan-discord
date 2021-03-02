
from discord import User, RawReactionActionEvent, PartialEmoji
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.context import Context

from config import config
from src.database import Database
from src.attendance.enums import Locations
from src.attendance import AttendanceRequest
from src.utils import Emoji


class WatchCog(commands.Cog):

    def __init__(self, bot: Bot, database: Database):
        self.bot: Bot = bot
        self.db: Database = database

