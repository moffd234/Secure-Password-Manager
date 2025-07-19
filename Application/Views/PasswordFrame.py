from tkinter import ttk
from typing import TYPE_CHECKING

from Application.Utils.HelperFunctions import get_all_passwords

if TYPE_CHECKING:
    from Application.Views.ParentWindow import ParentWindow


class PasswordFrame(ttk.Frame):

    def __init__(self, parent: ttk.Frame, controller: 'ParentWindow'):
        super().__init__(parent)
        self.controller = controller

        self.tree: ttk.Treeview = ttk.Treeview(self, columns=["site", "username", "password"], show="headings")
        style = ttk.Style()
        style.configure("Treeview", background="light blue", fieldbackground="light blue", foreground="black")

        self.tree.heading("site", text="Site")
        self.tree.heading("username", text="Username")
        self.tree.heading("password", text="Password")

        self.tree.column("site", width=150, anchor="w")
        self.tree.column("username", width=200, anchor="w")
        self.tree.column("password", width=200, anchor="w")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.display_creds()
        self.tree.bind("<Double-1>", self.copy_password)

    def display_creds(self) -> None:
        """
        Populates the Treeview with decrypted credentials from the JSON file.
        """
        credentials: dict[str, dict[str, str]] = get_all_passwords()

        if credentials:
            for site, creds in credentials.items():
                self.tree.insert("", "end", values=(site, creds["username"], creds["password"]))

    def copy_password(self, event) -> None:
        """
        Copies the password of the selected credential row to the system clipboard.

        Triggered by a double-click event on the Treeview. Retrieves the selected row's password,
        clears the clipboard, and appends the password for quick copying.
        """
        selected_item = self.tree.focus()

        if selected_item:
            values = self.tree.item(selected_item, 'values')

            if values:
                password = values[2]
                self.clipboard_clear()
                self.clipboard_append(password)
                self.update()
