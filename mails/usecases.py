from pathlib import Path
from simplemail import Email, SimpleMailException
from pritty_print import print_red, print_green
from typing import List
from metadata import METADATA_TEMPLATE, METADATA_TEMPLATE_OLD


def get_emails(folder: Path):
    emails = []
    for element in folder.iterdir():
        if not element.is_file():
            continue
        try:
            emails.append(Email(element))
            print_green(f"{element} +++")
        except SimpleMailException as e:
            print_red(f"{element}: {e} ---")
    return emails


def save_to_metadata(file_name: str, emails: List[Email]) -> None:
    with open(file_name, 'w') as file:
        for email in emails:
            text = METADATA_TEMPLATE.format(email.get_date(), email.get_id())
            file.write(f"{text}\n")


def save_to_metadata_old(file_name: str, emails: List[Email]) -> None:
    with open(file_name, 'w') as file:
        counter = 1
        for email in emails:
            text = METADATA_TEMPLATE_OLD.format(
                counter,
                email.get_id(),
                email.get_date(),
                email.get_sender(),
                ', '.join(email.get_receivers())
                )
            file.write(f"{text}\n")
            counter += 1
