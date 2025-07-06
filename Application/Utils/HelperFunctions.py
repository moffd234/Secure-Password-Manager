import re


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
