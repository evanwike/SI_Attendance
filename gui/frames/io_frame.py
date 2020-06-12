import tkinter as tk
from tkinter.font import Font
from tkinter import filedialog
import gui.styles as styles


class IOFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,
                         highlightbackground=styles.primary,
                         highlightthickness=styles.frame_border_width,
                         padx=styles.frame_padx,
                         pady=styles.frame_pady)

        # Labels
        labels = [tk.Label(self, text='Response Workbook:'),
                  tk.Label(self, text='Roster Workbook:'),
                  tk.Label(self, text='Output Path:')]
        for i, label in enumerate(labels):
            label.grid(row=i, column=0, sticky='e')

        # Text Inputs
        self.paths = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.entries = [tk.Entry(self, textvariable=self.paths[0], state='readonly'),
                        tk.Entry(self, textvariable=self.paths[1], state='readonly'),
                        tk.Entry(self, textvariable=self.paths[2], state='readonly')]
        for i, entry in enumerate(self.entries):
            entry.grid(row=i, column=1)

        # Set defaults to clear errors
        styles.default_highlight_bg = self.entries[0].cget('highlightbackground')
        styles.default_highlight_thickness = self.entries[0].cget('highlightthickness')

        # Buttons
        btn_font = Font(family=styles.btn_font)
        buttons = [tk.Button(self, text='Browse', width=10),
                   tk.Button(self, text='Browse', width=10),
                   tk.Button(self, text='Save As...', width=10)]
        for i, button in enumerate(buttons):
            button.bind(
                '<Button-1>',
                [self.browse_responses_path,
                 self.browse_rosters_path,
                 self.save_output_path][i])
            button['font'] = btn_font
            button.grid(row=i, column=2)

    def browse_responses_path(self, event: object) -> None:
        # TODO: Fix / to work with OSX and Windows
        # TODO: Remember to remove initialdirs
        self.clear_error(0)
        responses_path = tk.filedialog.askopenfilename(
            initialdir="/Users/Evan/SI_Attendance/data/Responses.xlsx",
            title="Select the Responses Workbook.",
            filetypes=(("Excel Workbook", "*.xlsx"), ("Excel 97-2004", "*.xls")))
        self.paths[0].set(responses_path)

    def browse_rosters_path(self, event: object) -> None:
        self.clear_error(1)
        roster_path = tk.filedialog.askopenfilename(
            initialdir="/Users/Evan/SI_Attendance/data/Attendance_S20.xlsx",
            title="Select the Rosters Workbook.",
            filetypes=(("Excel Workbook", "*.xlsx"), ("Excel 97-2004 Workbook", "*.xls")))
        self.paths[1].set(roster_path)

    def save_output_path(self, event: object) -> None:
        self.clear_error(2)
        output_path = filedialog.asksaveasfilename(
            initialdir="/Users/Evan/downloads/5.xlsx",
            title="Select where to save the output file.",
            filetypes=(("Excel Workbook", "*.xlsx"), ("Excel 97-2004 Workbook", "*.xls")))
        self.paths[2].set(output_path)

    def get_paths(self) -> list:
        return [path.get() for path in self.paths]

    def get_responses_path(self) -> str:
        return self.paths[0].get()

    def get_rosters_path(self) -> str:
        return self.paths[1].get()

    def get_output_path(self) -> str:
        return self.paths[2].get()

    def set_entry_error(self, i: int, e: Exception):
        entry = self.entries[i]
        entry.configure(
            highlightbackground=styles.error_highlight_bg,
            highlightthickness=styles.error_highlight_width)
        self.paths[i].set(e)

    def set_responses_error(self, e: Exception):
        self.set_entry_error(0, e)

    def set_rosters_error(self, e: Exception):
        self.set_entry_error(1, e)

    def set_output_error(self, e: Exception):
        self.set_entry_error(2, e)

    def clear_error(self, i: int):
        self.entries[i].configure(
            highlightbackground=styles.default_highlight_bg,
            highlightthickness=styles.default_highlight_thickness)
        # self.paths[i].set('')

    def clear_errors(self):
        for i in range(len(self.entries)):
            self.clear_error(i)

    def clear_paths(self):
        for path in self.paths:
            path.set('')

    def reset(self):
        self.clear_errors()
        self.clear_paths()
