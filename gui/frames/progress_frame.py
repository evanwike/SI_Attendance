import tkinter as tk
from tkinter import IntVar
from tkinter.ttk import Progressbar


class ProgressFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.progress = IntVar()
        self.progress.set(0)

        # Update to get width of master frame
        tk.Tk.update(master)
        progress_bar = tk.ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate',
            variable=self.progress,
            length=self.master.winfo_width())

        self.progress_bar = progress_bar

    def set_progress_bar(self, num_responses):
        self.progress_bar.configure(maximum=num_responses)

    def update_progress_bar(self):
        self.progress.set(self.progress.get() + 1)
        self.progress_bar.update()

    def reset(self):
        self.progress.set(0)
        self.progress_bar.destroy()

    def hide_progress_bar(self):
        self.progress_bar.pack_forget()

    def show_progress_bar(self):
        self.progress_bar.pack()
