
from collections import ChainMap
from typing import Dict
from .enums import Periods


class AttendanceMessagesList:

    def __init__(self):

        self.messages: Dict[str, dict] = {
            Periods.MORNING.value: {},
            Periods.LUNCH.value: {},
            Periods.NOON.value: {},
            Periods.EVENING.value: {}
        }

    def add(self, time: str, channel_id: int, message_id: int):
        self.messages[time][channel_id] = message_id

    def get(self, time: str) -> dict:
        return self.messages[time]

    def empty(self, time: str):
        self.messages[time] = {}

    def get_by_messages(self) -> dict:
        result = []

        for period, entries in self.messages.items():

            # Get the id of every message and create a list of periods
            message_ids = entries.values()
            periods = len(message_ids) * [period]

            # Create a dict of id:period
            result.append(dict(zip(message_ids, periods)))

        return dict(ChainMap(*result))
