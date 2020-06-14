from tkinter.ttk import Style
from .frames.io_frame import IOFrame
from .frames.options_frame import OptionsFrame
from .frames.progress_frame import ProgressFrame
from .frames.button_frame import ButtonFrame
from .frames.error_frame import ErrorFrame
from attendance.attendance import Attendance
from exceptions import *
import utils
import traceback


# TODO: Fix reset method
class GUI:
    def __init__(self):
        self.output_path = ''
        self.window = tk.Tk()
        self.window.title('SI Attendance')

        # Root frame for padding
        root = tk.Frame(self.window, width=500)
        root.grid(row=0, column=0, padx=20, pady=20)
        self.root = root

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

        error_frame = ErrorFrame(root)
        error_frame.grid(row=6, column=0, sticky='nsew')
        self.error_frame = error_frame

        root.mainloop()

    def run(self, event: object) -> None:
        # TODO: Validate paths
        # TODO: Validate week
        paths = self.io_frame.get_paths()
        self.io_frame.clear_errors()
        self.options_frame.clear_error()
        self.error_frame.clear_error()

        try:
            week = self.options_frame.get_week()
            attendance = Attendance(*paths, week, self.progress_frame)
            self.progress_frame.set_progress_bar(attendance.responses.get_num_responses())
            self.progress_frame.show_progress_bar()

            if attendance.run():
                self.success()

        except ResponsesPathError as e:
            self.error_frame.set_error(e)
            self.io_frame.set_responses_error()
        except RostersPathError as e:
            self.error_frame.set_error(e)
            self.io_frame.set_rosters_error()
        except OutputPathError as e:
            self.error_frame.set_error(e)
            self.io_frame.set_output_error()
        except ResponsesError as e:
            self.error_frame.set_error(e)
            self.io_frame.set_responses_error()
        except RostersError as e:
            self.error_frame.set_error(e)
            self.io_frame.set_rosters_error()
        except tk.TclError:
            self.error_frame.set_error(WeekTypeError('Please enter a valid week number.'))
            self.options_frame.set_week_error()
        except WeekRangeError as e:
            self.error_frame.set_error(e)
            self.options_frame.set_week_error()
        except Exception as e:
            traceback.print_tb(e.__traceback__)

    def success(self) -> None:
        self.output_path = self.io_frame.get_output_path()
        # Reveal open button
        self.button_frame.show_open_button()

    # FIXME: Throws week error when resetting, with valid default week number = 1
    def reset(self, event: object) -> None:
        self.io_frame.reset()
        self.options_frame.reset()
        self.progress_frame.reset()
        self.button_frame.reset()

    def open(self, event: object) -> None:
        utils.open_file(self.output_path)
