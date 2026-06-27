import os
import re
import pandas as pd


def load_csv(filepath):
    """
    Load a CSV file into a pandas DataFrame.

    Handles:
    - file not found
    - empty file
    - successful loading
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    if os.path.getsize(filepath) == 0:
        raise ValueError(f"File is empty: {filepath}")

    return pd.read_csv(filepath)


def clean_phone(phone):
    """
    Clean a phone number into a consistent 10-digit format.

    Examples:
    - "(123) 456-7890" -> "1234567890"
    - "123-456-7890" -> "1234567890"
    - "123.456.7890" -> "1234567890"

    Invalid inputs return None.
    """
    if phone is None:
        return None

    phone_str = str(phone).strip()

    if phone_str == "":
        return None

    digits = re.sub(r"\D", "", phone_str)

    # Remove leading country code if phone is 11 digits and starts with 1
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if len(digits) != 10:
        return None

    return digits


def validate_email(email):
    """
    Validate email format using a regular expression.

    Returns True for valid emails and False for invalid ones.
    """
    if email is None:
        return False

    email_str = str(email).strip()

    if email_str == "":
        return False

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(pattern, email_str) is not None