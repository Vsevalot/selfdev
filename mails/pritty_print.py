class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_green(string: str) -> None:
    print(f"{bcolors.OKGREEN}{string}{bcolors.ENDC}")


def print_red(string: str) -> None:
    print(f"{bcolors.FAIL}{string}{bcolors.ENDC}")


def print_cyan(string: str) -> None:
    print(f"{bcolors.OKCYAN}{string}{bcolors.ENDC}")