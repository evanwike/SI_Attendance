import tkinter as tk
from tkinter.font import Font
import gui.styles as styles


class FileFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        btn_open = tk.Button(self, text='Open', width=10)
        btn_save = tk.Button(self, text='Save As...', width=10)

        font = Font(family=styles.btn_font)
        btn_open['font'] = font
        btn_save['font'] = font

        btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_save.grid(row=1, column=0, sticky="ew", padx=5)
