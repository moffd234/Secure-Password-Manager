from tkinter import ttk, Canvas, PhotoImage

from Application.Utils.PlaceholderEntry import PlaceholderEntry

MAIN_LOGO = './Assets/logo.png'
WIN_WIDTH = 720
WIN_HEIGHT = 480
FONT = ("aerial", 8, "bold")


class HomeFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame, controller):
        super().__init__(parent)
        self.controller = controller

        # Canvas
        canvas_image = PhotoImage(file=MAIN_LOGO)
        canvas = Canvas(width=WIN_WIDTH / 2, height=WIN_HEIGHT / 2, bg='light blue', highlightthickness=0)
        canvas.create_image(180, 120, image=canvas_image)

        # Labels
        site_label = ttk.Label(self, text='Website', background="light blue", font=FONT)
        username_label = ttk.Label(self, text='Username/Email', background="light blue", foreground='black', font=FONT)
        password_label = ttk.Label(self, text='Password', background="light blue", font=FONT)

        # Entries
        site_entry = PlaceholderEntry(placeholder="Enter site name", width=50, bg="light green", font=FONT)
        username_entry = PlaceholderEntry(placeholder="Enter username", width=50, bg="light green", font=FONT)
        password_entry = PlaceholderEntry(placeholder="Enter Password", width=50, bg="light green", font=FONT)
        site_entry.focus()
