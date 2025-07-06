import os
from tkinter import ttk, PhotoImage, Canvas

from Application.Utils.PlaceholderEntry import PlaceholderEntry

HOME_LOGO = '../Assets/Home Logo.png'


class EntryFrame(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.canvas_image: PhotoImage = PhotoImage(file=HOME_LOGO)
        self.canvas: Canvas = Canvas(self, bg='light blue', highlightthickness=0, width=720, height=480)
        self.canvas.create_image(360, 240, image=self.canvas_image)

        self.password_entry: PlaceholderEntry = PlaceholderEntry(self, width=50, placeholder="Enter Password")
        self.confirm_password_entry: PlaceholderEntry = PlaceholderEntry(self, width=50, placeholder="Confirm Password")

        self.login_button: ttk.Button = ttk.Button(self, text="Login", width=15)
        self.create_account_button: ttk.Button = ttk.Button(self, text="Create Account", width=15)

        self.place_elements()

    def place_elements(self) -> None:
        self.canvas.place(relx=0.5, rely=0.5, anchor="center", width=720, height=480)

        if os.path.exists("../Data/Settings.json"):
            self.password_entry.place(relx=0.5, rely=0.65, anchor="center")
            self.login_button.place(relx=0.9, rely=0.65, anchor="center")

        else:
            self.password_entry.place(relx=0.5, rely=0.75, anchor="center")
            self.confirm_password_entry.place(relx=0.5, rely=0.8, anchor="center")
            self.create_account_button.place(relx=0.9, rely=0.8, anchor="center")
