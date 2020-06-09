import tkinter as tk
from tkinter.ttk import Style
from .frames.io_frame import IOFrame
from .frames.progress_frame import ProgressFrame
from attendance.attendance import Attendance
from attendance.exceptions import *
import utils


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('SI Attendance')

        tk.Label(self.window, text='2. Select input/output file locations.').grid(row=0, column=0, sticky='w',
                                                                                  padx=(5, 0),
                                                                                  pady=(10, 0))
        io_frame = IOFrame(self.window)
        io_frame.grid(row=1, column=0)
        self.io_frame = io_frame

        Style().theme_use('clam')   # Progress bar theme
        progress_frame = ProgressFrame(self.window)
        progress_frame.grid(row=2, column=0, sticky='e', pady=10, padx=10)
        self.progress_frame = progress_frame

        btn_open = tk.Button(self.window, text='Open', width=10)
        btn_open.bind('<Button-1>', self.open)
        btn_open.grid(row=3, column=0, sticky='w', pady=(0, 10), padx=(10, 0))
        btn_open.grid_forget()
        self.btn_open = btn_open

        btn_run = tk.Button(self.window, text='Run', width=10)
        btn_run.bind('<Button-1>', self.run)
        btn_run.grid(row=3, column=0, sticky='e', pady=(0, 10), padx=(0, 10))

        self.output_path = ''
        self.window.mainloop()

    def run(self, event: object) -> None:
        responses_path = self.io_frame.get_responses_path()
        rosters_path = self.io_frame.get_rosters_path()
        output_path = self.io_frame.get_output_path()

        try:
            attendance = Attendance(responses_path, rosters_path, output_path, self.progress_frame)
            self.progress_frame.set_progress_bar(attendance.responses.get_num_responses())

            if attendance.run():
                self.success()

        except ResponsesError as e:
            self.io_frame.set_responses_error(e)
        except RostersError as e:
            print('Rosters Error')
            print(e)
        except Exception as e:
            print(e)

    def success(self):
        self.output_path = self.io_frame.get_output_path()
        self.io_frame.clear_paths()
        # Reveal open button
        self.btn_open.grid(row=3, column=0, sticky='w', pady=(0, 10), padx=(10, 0))

    def open(self, event: object):
        open_file(self.output_path)
        self.output_path = ''
        # Hide open button
        self.btn_open.grid_forget()
