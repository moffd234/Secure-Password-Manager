import os.path
import unittest
from unittest.mock import patch, mock_open

from Application.Utils.HelperFunctions import *

FUNCTIONS_PATH = "Application.Utils.HelperFunctions"


class TestHelperFunctions(unittest.TestCase):

    def assert_open_error(self, mock_get_passwords, mock_open_file, mock_logging, actual):
        mock_get_passwords.assert_called_once()
        mock_open_file.assert_called_once()
        mock_logging.assert_called_once()
        self.assertFalse(actual)

    def setUp(self):
        download_path: Path = Path(os.path.join(os.path.expanduser('~'), 'Downloads'))
        self.export_file_path = download_path / get_unique_filename(download_path, "passwords")

    def test_is_password_valid_true(self):
        test_password: str = "validPassword123!"

        self.assertTrue(is_password_valid(test_password))

    def test_is_password_valid_exactly_8_chars(self):
        test_password: str = "validP1!"

        self.assertTrue(is_password_valid(test_password))

    def test_is_password_valid_too_short(self):
        test_password: str = "validPa"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_uppercase(self):
        test_password: str = "valid_password123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_lowercase(self):
        test_password: str = "VALID_PASSWORD123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_only_letters(self):
        test_password: str = "vAlIdPaSsWoRd"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_number(self):
        test_password: str = "validPassword!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_only_number(self):
        test_password: str = "12345678"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_special(self):
        test_password: str = "validPassword123"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_only_special(self):
        test_password: str = "!@#$%^&*("

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_space_char(self):
        test_password: str = "ValidPassword  123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_tab_char(self):
        test_password: str = "ValidPassword\t123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_empty_string(self):
        test_password: str = ""

        self.assertFalse(is_password_valid(test_password))

    def test_hash_password(self):
        password: str = "ValidPassword123!"
        hashed_password: str = hash_password(password)

        self.assertNotEqual(password, hashed_password)

    def test_hash_passwords_dont_match(self):
        password: str = "ValidPassword123!"
        hashed_password_one: str = hash_password(password)
        hashed_password_two: str = hash_password(password)

        self.assertNotEqual(hashed_password_one, hashed_password_two)

    @patch("bcrypt.gensalt", return_value=b"salt")
    @patch("bcrypt.hashpw", return_value=b"hashed_password")
    def test_hash_passwords_assert_calls(self, mock_hashpw, mock_gensalt):
        expected: str = "hashed_password"
        actual: str = hash_password("Password")

        mock_hashpw.assert_called_once_with(b"Password", mock_gensalt.return_value)
        mock_gensalt.assert_called_once()
        self.assertEqual(expected, actual)

    def test_verify_password_true(self):
        password: str = "ValidPassword123!"
        hashed_password: str = hash_password(password)

        actual: bool = verify_password(password, hashed_password)
        self.assertTrue(actual)

    def test_verify_password_false(self):
        password: str = "ValidPassword123!"
        hashed_password: str = hash_password(password)

        actual: bool = verify_password("password", hashed_password)
        self.assertFalse(actual)

    def test_verify_password_empty_string(self):
        password: str = "ValidPassword123!"
        hashed_password: str = hash_password(password)

        actual: bool = verify_password("", hashed_password)
        self.assertFalse(actual)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"settings": {"autofill": "enabled"}}))
    def test_autofill_valid(self, mock_file):
        expected: str = "enabled"
        actual: str = autofill()

        mock_file.assert_called_once()
        self.assertEqual(expected, actual)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"settings": {"NotSettings": "value"}}))
    def test_autofill_not_setup_yet(self, mock_file):

        result = autofill()
        mock_file.assert_called_once()
        self.assertIsNone(result)

    def tearDown(self):

        if os.path.exists(self.export_file_path):
            os.remove(self.export_file_path)