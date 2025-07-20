from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Application.Views.ParentWindow import ParentWindow


class ResetFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame, controller: 'ParentWindow', *args):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        reset_type: str = args[0]
