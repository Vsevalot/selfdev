from re import search, compile, findall
from pathlib import Path
from typing import Optional
from datetime import datetime
import argparse

PATTERNS = {
    "From_string": compile(r"From:[\s\S]+?>"),
    "To_string": compile(r"To:[\s\S]+?Subject: "),
    "Mail": compile(r"[<'].+?[>']"),
    "Date_string": compile(r"Date:.+"),
    "Message-ID_string": compile(r"Message-ID:.+>"),
    "Message-ID_data": compile(r"<.+>")
}

METADATA_FILENAME = "metadata.txt"

METADATA_TEMPLATE = """{})
Message-ID: {}
Дата отправки: {}
От: {}
Кому: {}"""


def is_email(potential_email: str) -> bool:
    if '@' in potential_email:
        return True
    return False


def get_from(eml_body: str) -> Optional[str]:
    match = search(PATTERNS["From_string"], eml_body)
    if not match:
        return None

    from_mail = get_mails(match[0])[0]
    if is_email(from_mail):
        return from_mail
    return None


def get_to(eml_body: str) -> Optional[str]:
    match = search(PATTERNS["To_string"], eml_body)
    if not match:
        return None

    to_mails = get_mails(match[0])
    for mail in to_mails:
        if not is_email(mail):
            return None
    return ', '.join(to_mails)


def get_mails(to_match: str) -> list:
    to_mails = []
    match = findall(PATTERNS["To_data"], to_match)
    for mail in match:
        if mail[1:-1] not in to_mails:  # [1:-1] without <> or '' for
            to_mails.append(mail[1:-1])  # <address@mail.com>
    return to_mails


def get_date(eml_body: str) -> Optional[str]:
    match = search(PATTERNS["Date_string"], eml_body)
    if not match:
        return None

    after_weekday = match[0].split(',')[1]
    date = ' '.join(after_weekday.split(' ')[:4])
    d = datetime.strptime(date, " %d %b %Y")
    return d.strftime("%d.%m.%Y")


def get_messageid(eml_body: str) -> Optional[str]:
    match = search(PATTERNS["Message-ID_string"], eml_body)
    if not match:
        return None

    match = search(PATTERNS["Message-ID_data"], match[0])
    return match[0]


def get_metadata(path_to_eml: Path) -> dict:
    metadata = {}
    with open(path_to_eml) as eml:
        body = eml.read()
        metadata["From"] = get_from(body)
        metadata["To"] = get_to(body)
        metadata["Date"] = get_date(body)
        metadata["Message-ID"] = get_messageid(body)
        return metadata


def is_valid_metadata(metadata: dict) -> bool:
    for key in metadata:
        if metadata[key] is None:
            return False
    return True


def get_script_args():
    script_description = "Scans folder for all files, tries to read it as "\
                         "email, collect metadata and save it to a " \
                         f"{METADATA_FILENAME} file"
    parser = argparse.ArgumentParser(description=script_description)

    parser.add_argument("path_to_emails_folder",
                        type=str,
                        help="path to folder that contains email files")
    return parser.parse_args()


def process_folder(path_to_email_folder):
    folder = Path(path_to_email_folder)
    if not folder.is_dir():
        raise ValueError(f"You must give path to a folder, "
                         f"got {folder} instead")

    files = []
    for element in folder.iterdir():
        if not element.is_file():
            print(f"Element: {element} can not be parsed")
        else:
            files.append(element)
    make_metadata_txt(files)


def make_metadata_txt(files: list):
    counter = 1
    with open(METADATA_FILENAME, 'w') as metadata_file:
        for file in files:
            try:
                email_metadata = get_metadata(file)
            except Exception as e:
                print(f"Can't get metadata from {file}. Error: {e}")
                continue

            if not is_valid_metadata(email_metadata):
                print(f"Can't collect all metadata from {file}")
                continue

            text = METADATA_TEMPLATE.format(counter,
                                            email_metadata["Message-ID"],
                                            email_metadata["Date"],
                                            email_metadata["From"],
                                            email_metadata["To"])
            metadata_file.write(f"{text}\n\n")
            counter += 1


if __name__ == '__main__':
    args = get_script_args()
    process_folder(args.path_to_emails_folder)
    print("Complete")
