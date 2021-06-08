from typing import Optional
from re import search, compile, match
from .validation import is_email


PATTERNS = {
    "Sender pattern": compile(r"From:[\w\W]*?<[\w\W]+?>"),
    "Receiver pattern": compile(r"To:[\w\W]+?(?=Subject: |CC: )"),
    "Date_string": compile(r"Date:.+"),
    "Message-ID_string": compile(r"Message-ID:.+>"),
    "Message-ID_data": compile(r"<.+>")
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
        return match[0][1:-1]
    return None


def sender_from_eml(eml_body: str) -> Optional[str]:
    """
    Gives email sender
    """
    match = search(PATTERNS["Sender pattern"], eml_body)
    if not match:
        return None

    sender_eml = get_bracket_content(match[0])
    if is_email(sender_eml):
        return sender_eml
    return None


def receiver_from_eml(eml_body: str) -> Optional[list[str]]:
    """
    Gives email sender
    """
    match = search(PATTERNS["Sender pattern"], eml_body)
    if not match:
        return None

    sender_eml = get_bracket_content(match[0])
    if is_email(sender_eml):
        return sender_eml
    return None


def date_from_eml(eml_body: str) -> Optional[str]:
    return


def message_id_from_eml(eml_body: str) -> Optional[str]:
    return
