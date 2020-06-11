import tkinter as tk
import gui.styles as styles


class OptionsFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,
                         highlightbackground=styles.primary,
                         highlightthickness=styles.frame_border_width,
                         padx=styles.frame_padx,
                         pady=styles.frame_pady)

        self.week = tk.IntVar()
        self.week.set(1)    # Default to week 1
        tk.Label(self, text='Week #:').grid(row=0, column=0)
        week_entry = tk.Entry(self, textvariable=self.week, width=10)
        week_entry.grid(row=0, column=1, sticky='w')
        self.week_entry = week_entry

    def get_week(self):
        return self.week.get()

    def set_week_error(self, e: Exception):
        self.week_entry.configure(
            highlightbackground=styles.error_highlight_bg,
            highlightthickness=styles.error_highlight_width)
        self.week.set(e)

    def clear_error(self):
        self.week_entry.configure(
            highlightbackground=styles.default_highlight_bg,
            highlightthickness=styles.default_highlight_thickness)

    def clear_week(self):
        self.week.set('')

    def reset(self):
        self.clear_error()
        self.clear_week()
