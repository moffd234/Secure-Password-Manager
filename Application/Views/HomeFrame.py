import secrets
import string
from tkinter import ttk, Canvas, PhotoImage, simpledialog

from Application.Utils.HelperFunctions import autofill, create_autofill
from Application.Utils.PlaceholderEntry import PlaceholderEntry

MAIN_LOGO = '../Assets/logo.png'
WIN_WIDTH = 720
WIN_HEIGHT = 480
FONT = ("aerial", 8, "bold")


class HomeFrame(ttk.Frame):
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

        # Entries
        self.site_entry = PlaceholderEntry(placeholder="Enter site name", width=50, bg="light green", font=FONT)
        self.username_entry = PlaceholderEntry(placeholder="Enter username", width=50, bg="light green", font=FONT)
        self.password_entry = PlaceholderEntry(placeholder="Enter Password", width=50, bg="light green", font=FONT)
        self.site_entry.focus()

        # Buttons
        self.search_button = ttk.Button(text="Search", width=15, command="")
        self.autofill_button = ttk.Button(text="Autofill", width=15, command="")
        self.gen_button = ttk.Button(text="Generate", width=15, command=self.generate_password)
        self.add_button = ttk.Button(text="Add", width=42, command="")

        self.place_elements()

    def place_elements(self):
        self.canvas.place(relx=0.5, rely=0.25, anchor="center")

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
        Handles the autofill logic for setting a default username.

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
                self.error_label.config(text="Autofill username not provided.")
                return None

            was_successful: bool = create_autofill(username)
            if not was_successful:
                self.error_label.config(text="Error creating autofill, please try again later.")
                return None

        self.error_label.config(text="")

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
