import tkinter


class PlaceholderEntry(tkinter.Entry):
    """
    A custom tkinter Entry widget that supports placeholder text.

    This class extends the standard tkinter Entry widget by adding support for
    placeholder text that appears in the input field when it is empty and not focused.
    The placeholder is automatically removed when the widget gains focus and restored
    if the input is left empty when focus is lost.

    :param master: The parent widget.
    :param placeholder: The placeholder text to display when the field is empty.
    :param color: The foreground color of the placeholder text.
    :param kwargs: Additional keyword arguments passed to the tkinter.Entry constructor.
    """
    def __init__(self, master=None, placeholder="", color='grey', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder: str = placeholder
        self.color: str = color
        self.default_fg_color: str = self.cget('foreground')

        # Bind functions on FocusIn and FocusOut
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.put_placeholder()

    def put_placeholder(self) -> None:
        """
        Inserts placeholder text in the entry and sets foreground color.
        :return: None
        """
        self.insert(0, self.placeholder)
        self['fg'] = self.color

    def focus_in(self, event) -> None:
        """
        Clears placeholder text in the entry if it is still showing on FocusIn.
        :param event: Event automatically passed by tkinter
        :return: None
        """
        if self['fg'] == self.color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, event=None) -> None:
        """
        Re-enters placeholder text in the entry if entry is empty on FocusOut.
        :param event: Event automatically passed by tkinter
        :return: None
        """
        if not self.get():
            self.put_placeholder()

    def get_real_value(self) -> str:
        """
        Returns the actual user input from the entry field, excluding placeholder text.

        :return: The input string, or an empty string if the entry contains only the placeholder.
        """
        value = self.get()
        return "" if value == self.placeholder else value

    def set_value(self, text: str) -> None:
        """
        Sets the value of the entry, bypassing placeholder logic.
        """
        self.delete(0, 'end')
        self.insert(0, text)
        self['fg'] = self.default_fg_color