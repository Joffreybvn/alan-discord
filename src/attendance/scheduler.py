
from discord import Client
from src.attendance import AttendanceMessage
from src.attendance.enums import Periods


class Scheduler:

    def __init__(self, client: Client):

        # Morning attendances
        AttendanceMessage(client, Periods.MORNING, (8, 50), (9, 00))

        # Lunch attendances
        AttendanceMessage(client, Periods.LUNCH, (12, 30), (13, 30))

        # Noon attendances
        AttendanceMessage(client, Periods.NOON, (13, 20), (13, 30))

        # Evening attendances
        AttendanceMessage(client, Periods.EVENING, (17, 00), (21, 00))

    @staticmethod
    def start():
        AttendanceMessage.start()
