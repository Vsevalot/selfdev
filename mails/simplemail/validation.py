from re import match, compile

EMAIL_PATTERN = compile(r'[\w.\-]+@[\w.\-]+\.\w{2,3}')


def is_email(potential_email: str) -> bool:
    if match(EMAIL_PATTERN, potential_email):
        return True
    return False
