import tkinter as tk
from tkinter.font import Font
from tkinter import filedialog
import gui.styles as styles


class IOFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.configure(
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
        self.responses_path = tk.StringVar()
        self.roster_path = tk.StringVar()
        self.output_path = tk.StringVar()

        entries = [tk.Entry(self, textvariable=self.responses_path, state='readonly'),
                   tk.Entry(self, textvariable=self.roster_path, state='readonly'),
                   tk.Entry(self, textvariable=self.output_path, state='readonly')]
        for i, entry in enumerate(entries):
            entry.grid(row=i, column=1)

        # Buttons
        btn_font = Font(family=styles.btn_font)
        buttons = [tk.Button(self, text='Browse', width=10),
                   tk.Button(self, text='Browse', width=10),
                   tk.Button(self, text='Save As...', width=10)]
        for i, button in enumerate(buttons):
            button.bind(
                '<Button-1>',
                [self.browse_responses_path,
                 self.browse_roster_path,
                 self.save_output_path][i])
            button['font'] = btn_font
            button.grid(row=i, column=2)

    def browse_responses_path(self, e):
        responses_path = tk.filedialog.askopenfilename(
            initialdir="/",
            title="Select the Responses Workbook.",
            filetypes=(("Excel Workbook", "*.xlsx"), ("Excel 97-2004", "*.xls")))
        self.responses_path = responses_path

    def browse_roster_path(self, e):
        roster_path = tk.filedialog.askopenfilename(
            initialdir="/",
            title="Select the Rosters Workbook.",
            filetypes=(("Excel Workbook", "*.xlsx"), ("Excel 97-2004 Workbook", "*.xls")))
        self.roster_path.set(roster_path)

    def save_output_path(self, e):
        output_path = filedialog.asksaveasfilename(
            initialdir="/",
            title="Select where to save the output file.",
            filetypes=(("Excel Workbook", "*.xlsx"), ("Excel 97-2004 Workbook", "*.xls")))
        self.output_path.set(output_path)

    def get_response_path(self):
        return self.responses_path

    def get_roster_path(self):
        return self.roster_path

    def get_output_path(self):
        return self.output_path
