import logging
import tkinter
from tkinter import ttk, messagebox

from Application.Utils.HelperFunctions import export_passwords
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
        # Account
        account_menu: tkinter.Menu = tkinter.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Account", menu=account_menu)
        account_menu.add_command(label="Reset App Password", command=lambda: self.render_frame(ResetFrame, "password"))
        account_menu.add_command(label="Change Autofill", command=lambda: self.render_frame(ResetFrame, "autofill"))
        account_menu.add_command(label="View Passwords", command=lambda: self.render_frame(PasswordFrame))
        account_menu.add_command(label="Export Passwords", command=export_passwords)

        account_menu.add_separator()
        account_menu.add_command(label="Home", command=lambda: self.render_frame(HomeFrame))
        account_menu.add_command(label="Exit", command=exit)

        # Settings
        settings_menu: tkinter.Menu = tkinter.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Theme", command="")

        self.configure(menu=self.menu_bar)

    @staticmethod
    def export_passwords() -> None:
        """
        Prompts the user for confirmation to export all stored passwords in unencrypted form.

        If the user consents, attempts to export the passwords to a file in the user's Downloads directory.
        Displays a success message if the export completes successfully, or an error message if it fails.

        The exported passwords file should be handled securely and deleted promptly to protect sensitive data.

        :return: None
        """
        answer: str = messagebox.askquestion("Export Passwords",
                                             "Doing this will export your passwords in unencrypted form."
                                             " Please delete the file as soon as you are done."
                                             " Do you wish to continue?")

        if answer == "yes":
            was_successful: bool = export_passwords()
            if not was_successful:
                messagebox.showerror("Export Failed", "Failed to export passwords.")
            else:
                messagebox.showinfo("Export Successful", "Successfully exported passwords.")

        return None


if __name__ == "__main__":
    app: ParentWindow = ParentWindow()
    logging.info("Application started")
    app.mainloop()
