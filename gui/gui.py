from tkinter.ttk import Style
from .frames.io_frame import IOFrame
from .frames.options_frame import OptionsFrame
from .frames.progress_frame import ProgressFrame
from .frames.button_frame import ButtonFrame
from attendance.attendance import Attendance
from exceptions import *
import utils


class GUI:
    def __init__(self):
        self.output_path = ''
        self.window = tk.Tk()
        self.window.title('SI Attendance')

        # Root frame for padding
        root = tk.Frame(self.window, width=500)
        root.grid(row=0, column=0, padx=20, pady=20)
        self.root = root

        # tk.Label(root, text='2. Select input/output file locations.').grid(row=0, column=0, sticky='w', pady=(10, 0))
        tk.Label(root, text='File I/O').grid(row=0, column=0, sticky='w')
        io_frame = IOFrame(root)
        io_frame.grid(row=1, column=0, sticky='nsew')
        self.io_frame = io_frame

        tk.Label(root, text='Options').grid(row=2, column=0, sticky='w', pady=(10, 0))
        options_frame = OptionsFrame(root)
        options_frame.grid(row=3, column=0, sticky='nsew')
        self.options_frame = options_frame

        Style().theme_use('clam')  # Progress bar theme
        progress_frame = ProgressFrame(root)
        progress_frame.grid(row=4, column=0, pady=10, sticky='nsew')
        self.progress_frame = progress_frame

        button_frame = ButtonFrame(self.open, self.reset, self.run, root)
        button_frame.grid(row=5, column=0, pady=(0, 10), sticky='nsew')
        self.button_frame = button_frame

        root.mainloop()

    def run(self, event: object) -> None:
        # TODO: Validate paths
        # TODO: Validate week
        paths = self.io_frame.get_paths()
        self.io_frame.clear_errors()
        self.options_frame.clear_error()

        try:
            week = self.options_frame.get_week()
            attendance = Attendance(*paths, week, self.progress_frame)
            self.progress_frame.set_progress_bar(attendance.responses.get_num_responses())
            self.progress_frame.show_progress_bar()

            if attendance.run():
                self.success()

        except ResponsesPathError as e:
            self.io_frame.set_responses_error(e)
        except RostersPathError as e:
            self.io_frame.set_rosters_error(e)
        except OutputPathError as e:
            self.io_frame.set_output_error(e)
        except ResponsesError as e:
            self.io_frame.set_responses_error(e)
        except RostersError as e:
            self.io_frame.set_rosters_error(e)
        except tk.TclError:
            self.options_frame.set_week_error(WeekTypeError('Invalid'))
        except WeekRangeError as e:
            self.options_frame.set_week_error(e)
        # except Exception as e:
        #     print(e)

    def success(self):
        self.output_path = self.io_frame.get_output_path()
        # Reveal open button
        self.button_frame.show_open_button()

    def reset(self, event: object) -> None:
        self.io_frame.reset()
        self.options_frame.reset()
        self.progress_frame.reset()
        self.button_frame.reset()

    def open(self, event: object) -> None:
        utils.open_file(self.output_path)
        # self.output_path = ''
