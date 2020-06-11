import tkinter as tk
import gui.styles as styles


class WeekFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,
                         highlightbackground=styles.primary,
                         highlightthickness=styles.frame_border_width,
                         padx=styles.frame_padx,
                         pady=styles.frame_pady)

        self.checked = tk.BooleanVar()
        chk_week = tk.Checkbutton(self, text='Week', variable=self.checked)