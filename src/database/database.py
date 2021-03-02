
from typing import List, Union

from pymongo import MongoClient
from mongoframes.queries import Q

from . import User, Watch, Channel


class Database:

    def __init__(self, db_host: str, db_password: str):
        self.client = MongoClient(f"mongodb+srv://dbUser:{db_password}@{db_host}")
        db_name = "discord"

        # Link frames to the database
        User._client = self.client
        Watch._client = self.client
        Channel._client = self.client

        User._db = db_name
        Watch._db = db_name
        Channel._db = db_name

    # ADMINISTRATION related queries
    # -------------------------------------------------------------------------

    @staticmethod
    def add_channel(channel_type: str, channel_id: int):
        """
        Add a channel id to a channel list. Create the channel list if it
        doesn't exists yet.

        :param channel_type: The name of the channel list. See the
            "CHANNEL_TYPES" in the config files for references.
        :param channel_id: The id of the channel to save.
        """

        channels = Channel.by_id(channel_type)

        # Create the channel list if it doesn't exists yet
        if channels is None:

            channels = Channel(
                _id=channel_type,
                channels=[]
            )

        # Add the new channel id
        if channel_id not in channels.channels:
            channels.channels.append(channel_id)

        # Upsert it to the database
        channels.upsert()

    @staticmethod
    def remove_channel(channel_type: str, channel_id: int):
        """
        Remove a channel id from a channel list.

        :param channel_type: The name of the channel list. See the
            "CHANNEL_TYPES" in the config files for references.
        :param channel_id: The id of the channel to remove.
        """

        channels = Channel.by_id(channel_type)

        # Do nothing if the channels doesn't exists
        if channels is None:
            return

        # Remove the channel id
        if channel_id in channels.channels:
            channels.channels.remove(channel_id)

        # Upsert it to the database
        channels.upsert()

    @staticmethod
    def get_channels(channel_type: str) -> List[int]:
        """Return a list of channel from a given channel_type."""

        # Get the channels
        channels = Channel.by_id(channel_type)

        # Return an empty list if the channel type doesn't exists yet
        if channels is None:
            return []

        return channels.channels

    # USER related queries
    # -------------------------------------------------------------------------

    @staticmethod
    def upsert_user(user_id: str, **kwargs):
        """
        Update or Insert a user to the database.

        :param user_id: The user to add to the database.
        :param kwargs:
            - send_notification (bool)
            - becode_token (str)
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
