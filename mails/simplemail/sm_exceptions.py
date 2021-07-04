

class SimpleMailException(Exception):
    pass


class SenderException(SimpleMailException):
    pass


class ReceiversException(SimpleMailException):
    pass


class DateException(SimpleMailException):
    pass


class ThemeException(SimpleMailException):
    pass


class IDException(SimpleMailException):
    pass
