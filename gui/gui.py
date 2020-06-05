import tkinter as tk
from gui.frames.frames import Frames


class GUI:
    def __init__(self):
        window = tk.Tk()
        self.window = window
        self.init_window()
        self.init_frames()

    def init_window(self):
        self.window.title('SI Attendance')
        self.window.minsize(400, 300)
        self.window.maxsize(800, 600)

    def init_frames(self):
        frames = Frames(self.window)
        file_frame = frames.get_file_frame()
        file_frame.grid(row=0, column=0, padx=10, pady=10)

    def run(self):
        self.window.mainloop()