import logging
import tkinter
from tkinter import ttk

from Application.Utils.LoggingController import setup_logging
from Application.Views.EntryFrame import EntryFrame


class ParentWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        setup_logging()
        self.title("Password Manager!")
        self.geometry("720x480")
        self.resizable(False, False)

        self.container: ttk.Frame = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
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


if __name__ == "__main__":
    app: ParentWindow = ParentWindow()
    logging.info("Application started")
    app.mainloop()
