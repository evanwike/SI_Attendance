import pandas as pd
import utils
from .responses import Responses
from .rosters import Rosters
from exceptions import *
from gui.frames.progress_frame import ProgressFrame
from xlsxwriter.utility import xl_range, xl_rowcol_to_cell


class Attendance:
    def __init__(self,
                 responses_path: str,
                 rosters_path: str,
                 output_path: str,
                 week: int,
                 progress_frame: ProgressFrame):
        self.output_path = output_path
        self.week = week
        self.progress_frame = progress_frame

        try:
            self.responses = Responses(responses_path)
        except OSError as e:
            raise ResponsesError(e.strerror)

        try:
            self.rosters = Rosters(rosters_path)
        except OSError as e:
            raise RostersError(e.strerror)

        # Validate week #
        upper_bound = self.rosters.get_week_bound()
        if self.week < 1 or self.week > upper_bound:
            raise WeekRangeError(f'Week must be in the range [1, {upper_bound}]')

    def parse_response(self, response: pd.Series):
        date, last, _id, course = response
        course = utils.format_course(course)

        print(f'Searching for: {last, _id, course}')

        if course in self.rosters.workbook:
            print(f'\tCourse found in attendance workbook: {course}')

            # 1. Search by _id in current course sheet
            row = self.rosters.search_sheet_by_id(_id, course)

            # Found student in current sheet
            if row is not None:
                # TODO: Validate responses match week
                # Ignore first 2 columns [ID, Name], OpenPyXl indexing starts from 1
                col = 2 + self.week
                # col = 2 + utils.get_week(date)
                self.rosters.increment_student(course, row, col)
            # Unable to find student in sheet, search other sheets
            else:
                print(f'\tSearching for student "{last}" in other sheets...')
                # TODO: This would be easier if I had session times - can't assume student in different course is the
                #  same, as they could be in multiple sessions.
        else:
            print(f'\tUnable to find course "{course}" in attendance workbook.')
            # TODO: Find most probable course student belongs to
        print()

        # Update progress bar
        # TODO: Make this include writing data to Excel
        self.progress_frame.update_progress_bar()

    def run(self) -> bool:
        self.responses.workbook.apply(self.parse_response, axis=1)

        with pd.ExcelWriter(self.output_path, engine='xlsxwriter') as writer:
            border = writer.book.add_format({'border': 1})
            border_center = writer.book.add_format({'border': 1, 'align': 'center'})
            percent = writer.book.add_format()
            percent.set_num_format(9)  # 0%

            # Manually write each cell in each sheet for formatting
            for course, df in self.rosters.workbook.items():
                # Convert string IDs back to ints
                df['ID'] = df['ID'].astype(int)

                df.to_excel(writer, sheet_name=course, index=False, header=False, startrow=1)
                worksheet = writer.sheets[course]

                # Fit Name and stats columns
                worksheet.set_column('B:B', max(df['Name'].str.len()))
                worksheet.set_column('M:M', 17)

                # Ignore last 3 columns (stats columns) for header
                header = df.columns.values[:-3].tolist()

                # Write header
                for i, val in enumerate(header):
                    worksheet.write(0, i, val, border_center)

                rows, cols = df.shape

                # For each column
                for i in range(cols - 4):     # Ignore last 3 (stats) columns and total column
                    col = df.iloc[:, i]
                    # For each row
                    for j, val in enumerate(col):
                        # Write cells
                        worksheet.write(j + 1, i,
                                        None if pd.isna(val) else val,          # Write value if value, else blank
                                        border if i < 2 else border_center)     # Only center cells after first 2 cols

                # Write formulas to Total column
                total_i = cols - 4          # FIXME: What if empty cols after?
                for i in range(1, rows + 1):
                    _range = xl_range(i, 2, i, total_i - 1)
                    worksheet.write_formula(i, total_i, f'=SUM({_range})', cell_format=border_center)

                # Write stats formulas
                # Total Students Seen
                range1 = xl_range(1, total_i, rows, total_i)
                worksheet.write_formula(1, cols - 1, f'=COUNTIF({range1}, ">0")')
                # % Students Seen
                range2 = xl_rowcol_to_cell(1, cols - 1)
                worksheet.write_formula(2, cols - 1, f'{range2}/{rows}', cell_format=percent)
                # Total Contact Hours
                worksheet.write_formula(3, cols - 1, f'=SUM({range1})')

            return True
