
from discord import Client
from src.database import Database
from src.attendance import AttendanceMessage
from src.attendance.enums import Periods


class Scheduler:

    def __init__(self, client: Client, database: Database):

        # Morning attendances
        AttendanceMessage(client, database, Periods.MORNING, (8, 50), (9, 00))

        # Lunch attendances
        AttendanceMessage(client, database, Periods.LUNCH, (12, 30), (13, 30))

        # Noon attendances
        AttendanceMessage(client, database, Periods.NOON, (13, 20), (13, 30))

        # Evening attendances
        AttendanceMessage(client, database, Periods.EVENING, (17, 00), (21, 00))

    @staticmethod
    def start():
        AttendanceMessage.start()
