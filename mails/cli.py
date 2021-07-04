from pritty_print import print_cyan
from metadata import METADATA_FILENAME
import argparse
from pathlib import Path
from usecases import get_emails, save_to_metadata, save_to_metadata_old


def get_script_args():
    script_description = "Scans folder for all files, tries to read it as "\
                         "email, collect metadata and save it to a " \
                         f"metadata file"
    parser = argparse.ArgumentParser(description=script_description)

    parser.add_argument("path_to_emails_folder",
                        type=str,
                        help="path to folder that contains email files")

    parser.add_argument("--metadata_file_name", "-m",
                        type=str,
                        default=METADATA_FILENAME,
                        help=f"name of the metadata file, default is "
                             f"{METADATA_FILENAME}")

    parser.add_argument("--old_format", "-o",
                        type=bool,
                        default=False,
                        help="Use old metadata format")
    return parser.parse_args()


def main():
    args = get_script_args()
    write_metadata_file(args)


def write_metadata_file(args: argparse.Namespace):
    file_name = args.metadata_file_name
    path_to_email_folder = args.path_to_emails_folder
    folder = Path(path_to_email_folder)
    if not folder.is_dir():
        raise ValueError(f"You must give path to a folder, "
                         f"got {folder} instead")
    emails = get_emails(folder)

    if args.old_format:
        save_to_metadata_old(file_name, emails)
    else:
        save_to_metadata(file_name, emails)

    print_cyan(f"{file_name} completed")


if __name__ == '__main__':
    main()
