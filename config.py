
from os import environ
from src.attendance import AttendanceMessagesList


class Config:

    def __init__(self):

        # Discord authentication
        self.TOKEN = environ.get('DISCORD_TOKEN')

        # MongoDB authentication
        self.DB_HOST = environ.get('DB_HOST')
        self.DB_PASSWORD = environ.get('DB_PASSWORD')

        # MS Bot Framework app
        self.BOT_API = environ.get('BOT_API')
        self.BOT_CALLBACK_PORT = int(environ.get('BOT_CALLBACK_PORT'))

        # My BeCode URL
        self.MY_BECODE_URL = "https://my.becode.org"

        # Channels where the bot listen to messages
        self.CHANNEL_WHITELIST = [
            815314932156858368
        ]

        # Channels where the bot publish attendance
        self.CHANNEL_ATTENDANCE = [
            815314932156858368
        ]

        self.ATTENDANCE_MESSAGES = AttendanceMessagesList()


config = Config()