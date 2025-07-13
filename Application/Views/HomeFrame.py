from tkinter import ttk, Canvas, PhotoImage

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
        self.username_label = ttk.Label(self, text='Username/Email', background="light blue", foreground='black', font=FONT)
        self.password_label = ttk.Label(self, text='Password', background="light blue", font=FONT)

        # Entries
        self.site_entry = PlaceholderEntry(placeholder="Enter site name", width=50, bg="light green", font=FONT)
        self.username_entry = PlaceholderEntry(placeholder="Enter username", width=50, bg="light green", font=FONT)
        self.password_entry = PlaceholderEntry(placeholder="Enter Password", width=50, bg="light green", font=FONT)
        self.site_entry.focus()

        # Buttons
        self.search_button = ttk.Button(text="Search", width=15, command="")
        self.autofill_button = ttk.Button(text="Autofill", width=15, command="")
        self.gen_button = ttk.Button(text="Generate", width=15, command="")
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