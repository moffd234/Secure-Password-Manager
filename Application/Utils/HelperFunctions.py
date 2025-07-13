import json
import re

import bcrypt


def is_password_valid(password: str) -> bool:
    """
    Checks if the password has the following requirements:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character

    :param password: password previously inputted by user
    :return: true if password is valid
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"
    return True if re.match(pattern, password) else False


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt with a generated salt.

    :param password: The plain-text password to hash.
    :return: A bcrypt-hashed version of the password.
    """
    encoded_bytes: bytes = password.encode('utf-8')
    salt: bytes = bcrypt.gensalt()
    hashed_password: bytes = bcrypt.hashpw(encoded_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """
    Verifies a plain-text password against a previously hashed password using bcrypt.

    :param password: The plain-text password to verify.
    :param hashed: The bcrypt-hashed password to compare against
    :return: True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def autofill() -> str | None:
    """
    Retrieves the autofill setting from the settings configuration file.

    Attempts to read the 'autofill' value from 'data/settings.json'. If the key does not exist,
    the function assumes autofill has not been configured and returns None.

    :return: The autofill value as a string, or None if the setting is not defined.
    """
    try:
        with open(file='data/settings.json', mode='r') as data_file:
            data = json.load(data_file)
            return data['settings']['autofill']
    except KeyError:
        # ASSERT: Autofill hasn't been setup yet
        return None
