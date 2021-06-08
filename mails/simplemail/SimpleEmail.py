from pathlib import Path
from .re_search import (sender_from_eml, receiver_from_eml,
                        date_from_eml, message_id_from_eml)


class Message():
    def __init__(self, path_to_eml: Path):
        with open(path_to_eml) as eml:
            body = eml.read()
            self.sender = sender_from_eml(body)
            self.receivers = receiver_from_eml(body)
            self.date = date_from_eml(body)
            self.message_id = message_id_from_eml(body)

    def __str__(self):
        return f"Email message. From:{self.sender}, To: {self.receiver}, " \
               f"date: {self.date}, message id: {self.message_id}"

    def __repr__(self):
        return self.__str__()
