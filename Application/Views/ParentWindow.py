import logging
import tkinter
from tkinter import ttk

from Application.Utils.LoggingController import setup_logging
from Application.Views.EntryFrame import EntryFrame
from Application.Views.PasswordFrame import PasswordFrame


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

    def render_frame(self, new_frame) -> None:
        """
        Destroys previous frame and renders new frame.
        :param new_frame: A new Frame object.
        :return: None
        """
        for frame in self.container.winfo_children():
            frame.destroy()

        frame: ttk.Frame = new_frame(self.container, self)

        frame.pack(fill="both", expand=True)

    def create_menu(self) -> None:
        """
        Creates the top menu bar for easier application navigation.
        :return: None
        """
        account_menu: tkinter.Menu = tkinter.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Account", menu=account_menu)
        account_menu.add_command(label="Reset App Password", command="")
        account_menu.add_command(label="Change Autofill", command="")
        account_menu.add_command(label="View Passwords", command=self.transition_to_password_frame)

        account_menu.add_separator()
        account_menu.add_command(label="Home", command=lambda: self.render_frame(EntryFrame))
        account_menu.add_command(label="Exit", command=exit)

        self.configure(menu=self.menu_bar)

    def transition_to_password_frame(self) -> None:
        """
        Transitions the current view to the PasswordFrame.
        """
        self.render_frame(PasswordFrame)


if __name__ == "__main__":
    app: ParentWindow = ParentWindow()
    logging.info("Application started")
    app.mainloop()
