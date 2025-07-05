from tkinter import ttk, PhotoImage, Canvas

from Application.Utils.PlaceholderEntry import PlaceholderEntry

HOME_LOGO = './Assets/Home Logo.png'


class EntryFrame(ttk.Frame):

    def __init__(self):
        super().__init__()

        canvas_image = PhotoImage(file=HOME_LOGO)
        self.canvas = Canvas(bg='light blue', highlightthickness=0, width=720, height=480)
        self.canvas.create_image(360, 240, image=canvas_image)

        self.password_entry: PlaceholderEntry = PlaceholderEntry(width=50, placeholder="Enter Password")
        self.confirm_password_entry: PlaceholderEntry = PlaceholderEntry(width=50, placeholder="Confirm Password")

        self.login: ttk.Button = ttk.Button(text="Login", width=15)
        self.create_account_button: ttk.Button = ttk.Button(text="Create Account", width=15)
