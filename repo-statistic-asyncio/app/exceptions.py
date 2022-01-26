class ArgumentException(Exception):
    def __init__(self, argument: str):
        self.argument = argument


class DateArgumentException(ArgumentException):
    def __repr__(self):
        return f"Can't parse argument {self.argument} to datetime." \
               f"Make sure the date is correct and " \
               f"use one of following formats: " \
               f"DD.MM.YY | DD.MM.YYYY | YYYY-MM-DD"
