from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Application.Views.ParentWindow import ParentWindow


class PasswordFrame(ttk.Frame):

    def __init__(self, parent: ttk.Frame, controller: 'ParentWindow'):
        super().__init__(parent)
        self.controller = controller