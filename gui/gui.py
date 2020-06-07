import tkinter as tk
from .frames.io_frame import IOFrame


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('SI Attendance')

        tk.Label(self.window, text='2. Select input/output file locations.').grid(row=0, column=0, sticky='w', padx=10)
        io_frame = IOFrame(self.window)
        io_frame.grid(row=1, column=0, padx=10)

    def run(self):
        self.window.mainloop()
