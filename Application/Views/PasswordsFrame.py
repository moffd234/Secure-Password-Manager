from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Application.Views.ParentWindow import ParentWindow


class PasswordsFrame(ttk.Frame):

    def __init__(self, controller: 'ParentWindow'):
        super().__init__()
        self.controller = controller