import json
import re
from json import JSONDecodeError

from cryptography.fernet import Fernet
import bcrypt

from Application.Utils.LoggingController import log_error_and_method

SETTINGS_FILE = "../.Data/Settings.json"
CRED_FILE = "../.Data/Creds.json"


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
        with open(file=SETTINGS_FILE, mode='r') as data_file:
            data = json.load(data_file)
            return data['settings']['autofill']
    except (FileNotFoundError, KeyError, JSONDecodeError) as error:
        log_error_and_method(error)
        # ASSERT: Autofill hasn't been setup yet
        return None


def create_autofill(username: str) -> bool:
    """
    Sets or updates the 'autofill' setting inside the 'settings' block of the config file.

    :param username: The username to store for autofill.
    :return: True if successful, False if file not found.
    """
    try:
        with open(SETTINGS_FILE, 'r') as data_file:
            data = json.load(data_file)

        data.setdefault('settings', {})['autofill'] = username

        with open(SETTINGS_FILE, 'w') as data_file:
            json.dump(data, data_file, indent=4)
            return True

    except (FileNotFoundError, JSONDecodeError) as error:
        log_error_and_method(error)
        return False


def store_creds(website: str, username: str, pwd: str) -> None:
    """
    Stores or updates login credentials for a given website in a JSON file.

    If the JSON file does not exist or is invalid, it will be created with the provided entry.
    If the file exists and is valid, the entry will be added or updated.

    :param website: The name of the website to associate with the credentials.
    :param username: The username or email to store.
    :param pwd: The password to store.
    :return: None
    """
    try:
        with open(file=CRED_FILE, mode='r') as data_file:
            data: dict = json.load(data_file)

    except (FileNotFoundError, JSONDecodeError) as error:
        log_error_and_method(error)
        with open(file=CRED_FILE, mode='w') as _:
            data: dict = {}

    data[website] = {"username": username, "password": pwd}

    with open(file=CRED_FILE, mode='w') as data_file:
        json.dump(data, data_file, indent=4)


def get_encryption_key() -> bytes:
    """
    Retrieves the symmetric encryption key used for encrypting and decrypting credentials.

    If the key file (`../.Data/secret.key`) exists, it loads and returns the key.
    If the key file is missing, a new Fernet key is generated, saved to the file,
    and then returned.

    :return: A Fernet-compatible encryption key as bytes.
    """

    key_path: str = "../.Data/secret.key"

    try:
        with open(key_path, "rb") as key_file:
            return key_file.read()

    except FileNotFoundError as error:
        log_error_and_method(error)
        key: bytes = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        return key


def check_entries(*args) -> bool:
    """
    Checks if all provided fields are non-empty.

    :param args: One or more strings representing input fields.
    :return: True if all fields are filled (non-empty), False otherwise.
    """

    return all(field for field in args)


def encrypt_password(pwd: str) -> str:
    """
    Encrypts a plain-text password using Fernet symmetric encryption.

    The password is encoded to bytes, encrypted using the Fernet key retrieved
    by `get_encryption_key()`, and then decoded back to a string for storage.

    :param pwd: The plain-text password to encrypt.
    :return: The encrypted password as a URL-safe base64-encoded string.
    """
    fernet: Fernet = Fernet(get_encryption_key())
    return fernet.encrypt(pwd.encode()).decode()


def decrypt_password(encrypted_pwd: str):
    """
    Decrypts an encrypted password string using Fernet symmetric encryption.

    The encrypted password string is encoded to bytes, decrypted using the Fernet key
    retrieved by `get_encryption_key()`, and then decoded back to the original plain-text password.

    :param encrypted_pwd: The encrypted password string to decrypt.
    :return: The original decrypted plain-text password.
    """
    fernet = Fernet(get_encryption_key())
    return fernet.decrypt(encrypted_pwd.encode()).decode()


def find_creds(site: str) -> dict[str, str] | None:
    """
    Searches credentials file for credentials matching the given site then returns the credentials if found.
    Otherwise, returns None.

    :param site: The website to search for credentials.
    :return: Username and decrypted password if found for the site. Otherwise, None.
    """
    try:
        with open(CRED_FILE, mode='r') as data_file:
            data: dict = json.load(data_file)
            creds: dict = data[site]
            creds["password"] = decrypt_password(creds["password"])
            return creds

    except (FileNotFoundError, KeyError, JSONDecodeError) as error:
        log_error_and_method(error)
        return None


def get_all_passwords() -> dict[str, dict[str, str]] | None:
    try:
        with open(CRED_FILE, mode='r') as data_file:
            data: dict[str, dict[str, str]] = json.load(data_file)

        for site in data:
            data[site]["password"] = decrypt_password(data[site]["password"])

        return data

    except (FileNotFoundError, KeyError, JSONDecodeError) as error:
        log_error_and_method(error)
        return None
