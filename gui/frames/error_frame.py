import tkinter as tk
import gui.styles as styles


class ErrorFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,
                         padx=styles.frame_padx,
                         pady=styles.frame_pady)

        self.error_msg = tk.StringVar()
        self.lbl_error = tk.Label(self, textvariable=self.error_msg, fg=styles.error_highlight_bg)
        self.lbl_error.grid(row=0, column=0)

    def set_error(self, error: Exception) -> None:
        self.error_msg.set('ERROR: ' + error.__str__())

    def clear_error(self):
        self.error_msg.set('')
