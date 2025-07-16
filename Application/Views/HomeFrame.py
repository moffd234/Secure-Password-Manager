import secrets
import string
from cryptography.fernet import Fernet
from tkinter import ttk, Canvas, PhotoImage, simpledialog

from Application.Utils.HelperFunctions import autofill, create_autofill, store_creds, get_encryption_key, check_entries
from Application.Utils.PlaceholderEntry import PlaceholderEntry

MAIN_LOGO = '../Assets/logo.png'
WIN_WIDTH = 720
WIN_HEIGHT = 480
FONT = ("aerial", 8, "bold")


class HomeFrame(ttk.Frame):
    """
    The main application frame for managing website credentials.

    This frame provides a user interface to input website, username, and password
    information, generate secure passwords, autofill saved usernames, and store
    hashed credentials securely in a JSON file.
    """

    def __init__(self, parent: ttk.Frame, controller):
        super().__init__(parent)
        self.controller = controller

        style = ttk.Style()
        style.configure("Blue.TFrame", background="light blue")
        self.configure(style="Blue.TFrame")

        # Canvas
        self.canvas_image = PhotoImage(file=MAIN_LOGO)
        self.canvas = Canvas(width=WIN_WIDTH / 2, height=WIN_HEIGHT / 2, bg='light blue', highlightthickness=0)
        self.canvas.create_image(180, 120, image=self.canvas_image)

        # Labels
        self.site_label = ttk.Label(self, text='Website', background="light blue", font=FONT)
        self.username_label = ttk.Label(self, text='Username/Email', background="light blue", foreground='black',
                                        font=FONT)
        self.password_label = ttk.Label(self, text='Password', background="light blue", font=FONT)
        self.error_label: ttk.Label = ttk.Label(self, background="light blue", foreground='red')
        self.success_label: ttk.Label = ttk.Label(self, background="light blue", foreground='green')

        # Entries
        self.site_entry = PlaceholderEntry(placeholder="Enter site name", width=50, bg="light green", font=FONT)
        self.username_entry = PlaceholderEntry(placeholder="Enter username", width=50, bg="light green", font=FONT)
        self.password_entry = PlaceholderEntry(placeholder="Enter Password", width=50, bg="light green", font=FONT)
        self.site_entry.focus()

        # Buttons
        self.search_button = ttk.Button(text="Search", width=15, command="")
        self.autofill_button = ttk.Button(text="Autofill", width=15, command=self.handle_autofill)
        self.gen_button = ttk.Button(text="Generate", width=15, command=self.generate_password)
        self.add_button = ttk.Button(text="Add", width=42, command="")

        self.place_elements()

    def place_elements(self):
        self.canvas.place(relx=0.5, rely=0.23, anchor="center")

        self.site_label.place(relx=0.22, rely=0.55, anchor="e")
        self.site_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.search_button.place(relx=0.83, rely=0.55, anchor="center")

        self.username_label.place(relx=0.22, rely=0.63, anchor="e")
        self.username_entry.place(relx=0.5, rely=0.63, anchor="center")
        self.autofill_button.place(relx=0.83, rely=0.63, anchor="center")

        self.password_label.place(relx=0.22, rely=0.71, anchor="e")
        self.password_entry.place(relx=0.5, rely=0.71, anchor="center")
        self.gen_button.place(relx=0.83, rely=0.71, anchor="center")

        self.add_button.place(relx=0.5, rely=0.82, anchor="center")

    def generate_password(self):
        """
        Generates a secure random password and sets it in the password entry field.

        The password consists of 15 characters randomly selected from uppercase letters,
        lowercase letters, digits, and punctuation symbols.

        :return: None
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(15))

        self.password_entry.set_value(password)

    def handle_autofill(self) -> None:
        """
        Handles the autofill logic for setting a default username or autofilling that username.

        Attempts to retrieve a previously saved autofill username. If none exists,
        prompts the user to enter a new one. If the user cancels or enters an invalid
        value, an error message is displayed. If a valid username is provided, it is
        saved to the settings. Displays an error if saving fails.

        :return: None
        """
        username: str | None = autofill()
        if not username:
            username = self.create_autofill_prompt()

            if not username:
                self.show_error("Error creating autofill, please try again later.")
                return None

            was_successful: bool = create_autofill(username)
            if not was_successful:
                self.show_error("Error creating autofill, please try again later.")
                return None

        self.username_entry.set_value(username)
        return None

    @staticmethod
    def create_autofill_prompt() -> str | None:
        """
        Prompt the user to create a default username for autofill.

        Shows an input dialog requesting a username. If the input is empty,
        repeatedly prompts the user until a non-empty username is provided or
        the dialog is canceled.

        :return: The entered username as a string, or None if the prompt was canceled.
        """
        result: str | None = simpledialog.askstring(title="Autofill Prompt",
                                                    prompt="Create a default username to autofill")

        while result is None or result == '':
            if result is None:
                # ASSERT: User canceled out of the prompt
                return None

            result = simpledialog.askstring(title="Username cannot be blank",
                                            prompt="Create a default username to autofill")

        return result

    def show_error(self, message: str):
        """
        Displays an error message centered on the screen for a limited duration.

        The message is shown in the error label widget, placed above all other widgets.
        It remains visible for 10 seconds before being automatically hidden.

        :param message: The error message to display.
        :type message: str
        :return: None
        """
        self.error_label.config(text=message)
        self.error_label.place(relx=0.5, rely=0.5, anchor="center")
        self.error_label.lift()

    def show_success(self, message: str):
        """
        Displays a success message centered on the screen.

        The message is shown in the success label widget, placed above all other widgets.
        It remains visible until manually cleared or replaced.

        :param message: The success message to display.
        :type message: str
        :return: None
        """
        self.success_label.config(text=message)
        self.success_label.place(relx=0.5, rely=0.5, anchor="center")
        self.success_label.lift()

    def add_creds(self) -> None:
        """
        Collects and stores user credentials for a given website.

        Retrieves the input from the website, username, and password entry fields.
        Encrypts the password using Fernet symmetric encryption and stores the resulting
        credentials in a JSON file via the `store_creds` helper function.

        If any required fields are empty, an error message is displayed and the process is aborted. Else a success
        message is displayed.

        :return: None
        """
        username: str = self.username_entry.get().strip()
        password: str = self.password_entry.get().strip()
        site: str = self.site_entry.get().strip()

        fernet: Fernet = Fernet(get_encryption_key())
        encrypted_pwd = fernet.encrypt(password.encode()).decode()

        if not check_entries(username, password, site):
            self.show_error("Please fill out all fields and try again.")
            return None

        store_creds(site, username, encrypted_pwd)
        self.show_success("Successfully stored credentials.")
        return None

    def clear_fields(self) -> None:
        """
        Clears the content of all input fields and restores their placeholder text.

        This method resets the site, username, and password entry fields to their initial state.

        :return: None
        """
        self.site_entry.clear_field()
        self.username_entry.clear_field()
        self.password_entry.clear_field()
