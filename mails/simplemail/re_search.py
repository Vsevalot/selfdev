from typing import Optional, List, Set
from re import search, compile
from datetime import datetime
from .validation import is_email
from .sm_exceptions import (SenderException, ReceiversException,
                            DateException, IDException)


PATTERNS = {
    "Sender field": compile(r"From:[\w\W]*?<[\w\W]+?>"),
    "Receiver field": compile(r"To:[\w\W]+?(?=Subject: |CC: )"),
    "Date field": compile(r"Date:.+"),
    "date": compile(r"\w+, \d{1,2} \w+ \d{4} \d{1,2}:\d{1,2}:\d{1,2}"),
    "Subject field": compile(r"Subject: .+"),
    "Message-ID field": compile(r"Message-ID: <.+>")
}


def get_bracket_content(string_with_brackets: str,
                        first_bracket: str = '<',
                        last_bracket: str = '>') -> Optional[str]:
    """
    Gives content inside specified brackets
    """
    pattern = f"{first_bracket}[\\w\\W]+{last_bracket}"
    match = search(pattern, string_with_brackets)
    if match:
        return match[0][len(first_bracket):-len(last_bracket)]
    return None


def get_sender_from_eml(eml_body: str) -> str:
    """
    Gives email sender
    Raises:
        SenderException
    """
    match = search(PATTERNS["Sender field"], eml_body)
    if not match:
        raise SenderException("Can't find sender!")

    sender_eml = get_bracket_content(match[0])
    if is_email(sender_eml):
        return sender_eml
    raise SenderException(f"Sender field is not an email: {sender_eml}")


def get_receivers_from_eml(eml_body: str) -> Set[str]:
    """
    Gives a list of email receivers
    Raises:
        ReceiversException
    """
    match = search(PATTERNS["Receiver field"], eml_body)
    if not match:
        raise ReceiversException("Can't find receivers!")

    receivers = get_receivers(match[0])

    for receiver in receivers:
        if not is_email(receiver):
            raise ReceiversException(f"Receiver is not an email: {receiver}")
    return receivers


def get_receivers(receiver_string: str) -> Set[str]:
    """
    Gives a list of receivers from the given string with To field value
    Raises:
        ReceiversException
    """
    receivers = set()
    for split_receiver in receiver_string.split(','):
        receiver = get_bracket_content(split_receiver)
        if receiver is not None:
            receivers.add(receiver)
    if not receivers:
        raise ReceiversException(f"No receivers found in: {receiver_string}")
    return receivers


def get_subject_from_eml(eml_body: str) -> str:
    """
    Gives subject or empty string if not found of the eml
    """
    match = search(PATTERNS["Subject field"], eml_body)
    if match:
        return get_subject(match[0])
    return ''


def get_subject(subject_field: str) -> str:
    return subject_field.replace("Subject: ", '')


def get_date_from_eml(eml_body: str) -> datetime:
    """
    Gives datetime date of the eml
    Raises:
        DateException
    """
    match = search(PATTERNS["Date field"], eml_body)
    if not match:
        raise DateException("Can't find date!")

    return get_datetime(match[0])


def get_datetime(date_string: str) -> datetime:
    if not match_date_pattern(date_string):
        raise DateException(f"Date field: {date_string} doesn't match "
                            f"the pattern {PATTERNS['date']}")
    after_weekday = date_string.split(',')[1]
    date = ' '.join(after_weekday.split(' ')[:4])
    return datetime.strptime(date, " %d %b %Y")


def match_date_pattern(date_string: str) -> bool:
    if search(PATTERNS["date"], date_string):
        return True
    return False


def get_message_id_from_eml(eml_body: str) -> str:
    """
    Gives Message-id date of the eml
    Raises:
        IDException
    """
    match = search(PATTERNS["Message-ID field"], eml_body)
    if not match:
        raise IDException("Can't find Message-ID!")

    message_id = get_bracket_content(match[0])
    if message_id is not None:
        return message_id
    raise IDException(f"Message-ID field error. Field value: {match[0]}")
