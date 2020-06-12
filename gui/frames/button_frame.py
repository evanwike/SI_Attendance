import tkinter as tk
import gui.styles as styles


class ButtonFrame(tk.Frame):
    def __init__(self,
                 _open: callable,
                 reset: callable,
                 run: callable,
                 master=None):
        super().__init__(master, pady=styles.frame_pady)

        btn_reset = tk.Button(self, text='Reset', width=10)
        btn_reset.bind('<Button-1>', reset)
        btn_reset.pack(side='left')

        btn_open = tk.Button(self, text='Open', width=10)
        btn_open.bind('<Button-1>', _open)
        self.btn_open = btn_open

        btn_run = tk.Button(self, text='Run', width=10)
        btn_run.bind('<Button-1>', run)
        btn_run.pack(side='right')

    def hide_open_button(self):
        self.btn_open.pack_forget()

    def show_open_button(self):
        self.btn_open.pack(side='left')

    def reset(self):
        self.hide_open_button()
