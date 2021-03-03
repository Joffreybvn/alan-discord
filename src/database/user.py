
from mongoframes.frames import Frame


class User(Frame):

    _fields = {
        # Discord id
        "_id",

        # BeCode token
        "becode_token"
        
        # Bot settings
        "send_notification"
        
        # Alan dashboard access
        "site_token"
        "site_token_timeout"
        "access_token"
        "access_token_timeout"
    }
