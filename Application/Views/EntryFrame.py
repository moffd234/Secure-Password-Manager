import json
import os
from tkinter import ttk, PhotoImage, Canvas

from Application.Utils.HelperFunctions import is_password_valid, hash_password
from Application.Utils.PlaceholderEntry import PlaceholderEntry

HOME_LOGO = '../Assets/Home Logo.png'


class EntryFrame(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.canvas_image: PhotoImage = PhotoImage(file=HOME_LOGO)
        self.canvas: Canvas = Canvas(bg='light blue', highlightthickness=0, width=720, height=480)
        self.canvas.create_image(360, 240, image=self.canvas_image)

        self.password_entry: PlaceholderEntry = PlaceholderEntry(width=50, placeholder="Enter Password")
        self.confirm_password_entry: PlaceholderEntry = PlaceholderEntry(width=50, placeholder="Confirm Password")

        self.login_button: ttk.Button = ttk.Button(text="Login", width=15)
        self.create_account_button: ttk.Button = ttk.Button(text="Create Account", width=15,
                                                            command=self.create_account)

        self.place_elements()

    def place_elements(self) -> None:
        self.canvas.place(relx=0.5, rely=0.5, anchor="center", width=720, height=480)

        if os.path.exists("../.Data/Settings.json"):
            self.password_entry.place(relx=0.5, rely=0.65, anchor="center")
            self.login_button.place(relx=0.9, rely=0.65, anchor="center")

        else:
            self.password_entry.place(relx=0.5, rely=0.75, anchor="center")
            self.confirm_password_entry.place(relx=0.5, rely=0.8, anchor="center")
            self.create_account_button.place(relx=0.9, rely=0.8, anchor="center")

    def create_account(self) -> None:
        password: str = self.password_entry.get()
        conf_password: str = self.confirm_password_entry.get()
        is_valid: bool = self.validate_passwords(password, conf_password)

        if is_valid:
            self.create_settings(password)
            return None

        else:
            return None

    @staticmethod
    def validate_passwords(password: str, conf_password: str) -> bool:
        if password != conf_password:
            return False

        if not is_password_valid(password):
            return False

        return True

    @staticmethod
    def create_settings(password: str) -> None:
        os.makedirs("../.Data", exist_ok=True)

        with open(file="../.Data/Settings.json", mode="w") as file:
            hashed_pass: str = hash_password(password)

            data: dict = {
                "pwd": hashed_pass,
            }
            json_str: str = json.dumps(data, indent=4)
            file.write(json_str)
