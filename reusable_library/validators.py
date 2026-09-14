import re
from datetime import datetime


def validate_required(value):
    #Check that a required value is not empty.
    return bool(value and value.strip())


def validate_email(email):
    #Check whether an email has a valid basic format.
    if not email:
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


def validate_password(password, minimum_length=4):
    #Check whether a password meets the minimum length.
    if not password:
        return False

    return len(password) >= minimum_length


def validate_date(date_text, date_format="%Y-%m-%d"):
    #Check whether a date matches the expected format.
    try:
        datetime.strptime(date_text, date_format)
        return True
    except (ValueError, TypeError):
        return False