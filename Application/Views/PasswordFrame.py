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

    def display_creds(self) -> None:
        credentials: dict[str, dict[str, str]] = get_all_passwords()

        if credentials:
            for site, creds in credentials.items():
                self.tree.insert("", "end", values=(site, creds["username"], creds["password"]))