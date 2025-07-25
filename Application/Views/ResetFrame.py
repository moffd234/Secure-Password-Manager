from tkinter import ttk, PhotoImage, Canvas
from typing import TYPE_CHECKING

from Application.Utils.PlaceholderEntry import PlaceholderEntry

if TYPE_CHECKING:
    from Application.Views.ParentWindow import ParentWindow

HOME_LOGO = '../Assets/Home Logo.png'

class ResetFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame, controller: 'ParentWindow', *args):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        reset_type: str = args[0]

        self.canvas_image: PhotoImage = PhotoImage(file=HOME_LOGO)
        self.canvas: Canvas = Canvas(self, bg='light blue', highlightthickness=0, width=720, height=480)
        self.canvas.create_image(360, 240, image=self.canvas_image)

        self.password_entry: PlaceholderEntry = PlaceholderEntry(self, width=50, placeholder=f"Enter {reset_type}")
        self.confirm_password_entry: PlaceholderEntry = PlaceholderEntry(self, width=50, placeholder=f"Confirm {reset_type}")

        self.login_button: ttk.Button = ttk.Button(self, text=f"Reset {reset_type}", width=15, command="")

        self.place_elements()

    def place_elements(self) -> None:
        """
        Places widgets on the frame
        """
        self.canvas.place(relx=0.5, rely=0.5, anchor="center", width=720, height=480)
        self.password_entry.place(relx=0.5, rely=0.75, anchor="center")
        self.confirm_password_entry.place(relx=0.5, rely=0.8, anchor="center")
        self.login_button.place(relx=0.9, rely=0.8, anchor="center")