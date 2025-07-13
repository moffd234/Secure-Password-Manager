import json
import os
from tkinter import ttk, PhotoImage, Canvas

from Application.Utils.HelperFunctions import is_password_valid, hash_password, verify_password
from Application.Utils.PlaceholderEntry import PlaceholderEntry

HOME_LOGO = '../Assets/Home Logo.png'


class EntryFrame(ttk.Frame):
    """
    Frame for handling password entry and account creation/login logic.
    Displays either login or account creation UI depending on whether settings exist.
    """

    def __init__(self, parent: ttk.Frame, controller):
        """
        Initialize the EntryFrame.

        :param controller: The controller managing frame transitions.
        :type controller: tkinter.Tk or any parent with `render_frame` method.
        """
        super().__init__(parent)

        self.controller = controller

        self.canvas_image: PhotoImage = PhotoImage(file=HOME_LOGO)
        self.canvas: Canvas = Canvas(self, bg='light blue', highlightthickness=0, width=720, height=480)
        self.canvas.create_image(360, 240, image=self.canvas_image)

        self.password_entry: PlaceholderEntry = PlaceholderEntry(self, width=50, placeholder="Enter Password")
        self.confirm_password_entry: PlaceholderEntry = PlaceholderEntry(self, width=50, placeholder="Confirm Password")

        self.login_button: ttk.Button = ttk.Button(self, text="Login", width=15)
        self.create_account_button: ttk.Button = ttk.Button(self, text="Create Account", width=15,
                                                            command=self.create_account)

        self.error_label: ttk.Label = ttk.Label(self, foreground="red")

        self.place_elements()

    def place_elements(self) -> None:
        """
       Places widgets on the frame depending on whether account settings exist.
       If settings exist, shows login UI; otherwise, shows account creation UI.
       """
        self.canvas.place(relx=0.5, rely=0.5, anchor="center", width=720, height=480)

        if os.path.exists("../.Data/Settings.json"):
            self.password_entry.place(relx=0.5, rely=0.65, anchor="center")
            self.login_button.place(relx=0.9, rely=0.65, anchor="center")

        else:
            self.password_entry.place(relx=0.5, rely=0.75, anchor="center")
            self.confirm_password_entry.place(relx=0.5, rely=0.8, anchor="center")
            self.create_account_button.place(relx=0.9, rely=0.8, anchor="center")

    def create_account(self) -> None:
        """
        Handles the logic for creating a new account.
        Validates password fields, saves hashed password, and redirects to the HomeFrame.
        Displays error if validation fails.
        """
        from HomeFrame import HomeFrame
        password: str = self.password_entry.get()
        conf_password: str = self.confirm_password_entry.get()
        is_valid: bool = self.validate_passwords(password, conf_password)

        if is_valid:
            self.create_settings(password)
            self.controller.render_frame(HomeFrame)
            return None

        self.error_label.config(text="Password is not valid")
        self.error_label.place(relx=0.4, rely=0.9)
        return None

    def is_password_correct(self) -> None:
        """
        Verifies the entered password against the stored hash.
        If verified, redirects to the HomeFrame.
        """
        from HomeFrame import HomeFrame
        pwd: str = self.password_entry.get()

        with open(file="../Data/Settings.json", mode="r") as file:
            data: dict = json.load(file)
            hashed_pwd: str = data["pwd"]
            if verify_password(password=pwd, hashed=hashed_pwd):
                self.controller.render_frame(HomeFrame)
                return None

        return None

    @staticmethod
    def validate_passwords(password: str, conf_password: str) -> bool:
        """
       Validates that the password matches the confirmation and passes meets complexity requirements.

       :param password: The main password entered by the user.
       :param conf_password: The confirmation password entered by the user.
       :return: True if passwords match and are valid, False otherwise.
       """
        if password != conf_password:
            return False

        if not is_password_valid(password):
            return False

        return True

    @staticmethod
    def create_settings(password: str) -> None:
        """
        Hashes the provided password and stores it in a local settings JSON file.

        :param password: The password to store securely.
        """
        os.makedirs("../.Data", exist_ok=True)

        with open(file="../.Data/Settings.json", mode="w") as file:
            hashed_pass: str = hash_password(password)

            data: dict = {"pwd": hashed_pass, }
            json_str: str = json.dumps(data, indent=4)
            file.write(json_str)
