import unittest

from Application.Utils.HelperFunctions import is_password_valid


class TestHelperFunctions(unittest.TestCase):

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
