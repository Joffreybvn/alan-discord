
from typing import List, Union

from pymongo import MongoClient
from mongoframes.queries import Q

from . import User


class Database:

    def __init__(self, db_host: str, db_password: str):
        self.client = MongoClient(f"mongodb+srv://dbUser:{db_password}@{db_host}")

        # Link frames to the database
        User._client = self.client
        User._db = "discord"

    @staticmethod
    def upsert_user(user_id: str, send_notification: bool = False, becode_token: str = None):
        """
        Update or Insert a user to the database.

        :param user_id: The user to add to the database.
        :param send_notification:
        :param becode_token:
        """

        # Create a User object
        user = User(
            _id=user_id,
            send_notification=send_notification,
            becode_token=becode_token
        )

        # Upsert it to the database
        user.upsert()

    @staticmethod
    def get_pingable_users() -> List[str]:
        """Return a list of all user to notify on attendance request."""

        # Query the database
        users = User.many((Q.send_notification == True).to_dict())

        # Return a list of all users' _id
        return [user['_id'] for user in list(users)]

    @staticmethod
    def get_token(user_id: str) -> Union[None, str]:
        """Return the token of a given user."""

        # Query the database
        user = User.one(Q._id == user_id, projection={'becode_token': True})

        # Return the BeCode token
        return user.__dict__['_document'].get('becode_token', None)
