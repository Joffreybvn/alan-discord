
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
    def upsert_user(user_id: str, **kwargs):
        """
        Update or Insert a user to the database.

        :param user_id: The user to add to the database.
        """

        document = dict(_id=user_id)

        # Update "send_notification" if provided
        if 'send_notification' in kwargs:
            document['send_notification'] = kwargs['send_notification']

        # Update "becode_token" if provided
        if 'becode_token' in kwargs:
            document['becode_token'] = kwargs['becode_token']

        user = User(**document)

        # Upsert it to the database
        user.upsert()

    @staticmethod
    def get_pingable_users() -> List[str]:
        """Return a list of all user to notify on attendance request."""

        # Query the database
        users = User.many(Q.send_notification == True)

        # Return a list of all users' _id
        return [user['_id'] for user in users]

    @staticmethod
    def get_token(user_id: str) -> Union[None, str]:
        """Return the token of a given user."""

        # Query the database
        user = User.one(Q._id == user_id, projection={'becode_token': True})

        # Return the BeCode token
        return user.__dict__['_document'].get('becode_token', None)
