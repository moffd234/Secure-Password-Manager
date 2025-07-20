import logging
import tkinter
from tkinter import ttk

from Application.Utils.LoggingController import setup_logging
from Application.Views.EntryFrame import EntryFrame
from Application.Views.HomeFrame import HomeFrame
from Application.Views.PasswordFrame import PasswordFrame
from Application.Views.ResetFrame import ResetFrame


class ParentWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        setup_logging()
        self.title("Password Manager!")
        self.geometry("720x480")
        self.resizable(False, False)

        self.container: ttk.Frame = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.menu_bar: tkinter.Menu = tkinter.Menu()
        self.render_frame(EntryFrame)

    def render_frame(self, new_frame, *args) -> None:
        """
        Destroys previous frame and renders new frame.
        :param new_frame: A class reference to the new ttk.Frame to render
        :param args: Optional arguments passed to the new frame's constructor.
        :return: None
        """
        for frame in self.container.winfo_children():
            frame.destroy()

        frame: ttk.Frame = new_frame(self.container, self, *args)

        frame.pack(fill="both", expand=True)

    def create_menu(self) -> None:
        """
        Creates the top menu bar for easier application navigation.
        :return: None
        """
        account_menu: tkinter.Menu = tkinter.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Account", menu=account_menu)
        account_menu.add_command(label="Reset App Password", command=lambda: self.render_frame(ResetFrame, "password"))
        account_menu.add_command(label="Change Autofill", command="")
        account_menu.add_command(label="View Passwords", command=lambda: self.render_frame(PasswordFrame))

        account_menu.add_separator()
        account_menu.add_command(label="Home", command=lambda: self.render_frame(HomeFrame))
        account_menu.add_command(label="Exit", command=exit)

        self.configure(menu=self.menu_bar)


if __name__ == "__main__":
    app: ParentWindow = ParentWindow()
    logging.info("Application started")
    app.mainloop()
