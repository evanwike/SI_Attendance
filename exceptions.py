import tkinter as tk


class ResponsesError(OSError):
    def __init__(self, e: str):
        self.e = e

    def __str__(self):
        return self.e


class ResponsesPathError(ResponsesError):
    def __init__(self, e: str):
        super().__init__(e)


class RostersError(OSError):
    def __init__(self, e: str):
        self.e = e

    def __str__(self):
        return self.e


class RostersPathError(RostersError):
    def __init__(self, e: str):
        super().__init__(e)


class OutputError(OSError):
    def __init__(self, e: str):
        self.e = e

    def __str__(self):
        return self.e


class OutputPathError(OutputError):
    def __init__(self, e: str):
        super().__init__(e)


class WeekTypeError(tk.TclError):
    def __init__(self, e: str):
        super().__init__(e)


class WeekRangeError(Exception):
    def __init__(self, e: str):
        super().__init__(e)
