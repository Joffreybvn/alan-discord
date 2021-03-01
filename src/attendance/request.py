
import aiohttp

from src.attendance.enums import Locations, Periods

# URL = "https://postman-echo.com/post"
URL = "https://graph.becode.org/"


class AttendanceRequest:

    def __init__(self, period: str, at_home: Locations, token: str):

        self.period: str = Periods(period).name
        self.at_home: bool = at_home.value[1]
        self.token: str = token

    def get_json(self) -> dict:

        return {
            "operationName": "record_attendance_time",
            "variables": {
                "period": self.period,
                "atHome": self.at_home
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "553ae433516c13a97e348d4a48dd0114d1949f791ab21d97bed27030a65e85a8"
                }
            }
        }

    async def send(self):

        headers = {"Authorization": f"Bearer {self.token}"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(URL, json=self.get_json()) as response:

                if response.status == 200:
                    body = await response.json()

                    try:
                        if body['data']['recordAttendanceTime']:
                            return True

                    except KeyError:
                        pass

        return False
