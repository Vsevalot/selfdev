from pathlib import Path
from .re_search import (get_sender_from_eml, get_receivers_from_eml,
                        get_date_from_eml, get_message_id_from_eml,
                        get_subject_from_eml)
from .sm_exceptions import SimpleMailException
from typing import Set


class Email():
    def __init__(self, path_to_eml: Path):
        self.body = get_body(path_to_eml)
        self.sender = get_sender_from_eml(self.body)
        self.receivers = get_receivers_from_eml(self.body)
        self.subject = get_subject_from_eml(self.body)
        self.date = get_date_from_eml(self.body)
        self.message_id = get_message_id_from_eml(self.body)

    def get_id(self) -> str:
        return self.message_id

    def get_sender(self) -> str:
        return self.sender

    def get_receivers(self) -> Set[str]:
        return self.receivers

    def get_subject(self):
        return self.subject

    def get_date(self):
        return self.date.strftime("%d.%m.%Y")

    def __str__(self):
        return f"Email message. From:{self.sender}, " \
               f"To: {*self.receivers, }, " \
               f"date: {self.date}, message id: {self.message_id}"

    def __repr__(self):
        return self.__str__()


def get_body(path_to_eml: Path) -> str:
    with open(path_to_eml) as eml:
        return eml.read()
