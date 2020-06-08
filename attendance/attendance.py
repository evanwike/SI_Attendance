import pandas as pd
import datetime
import logging
from .responses import Responses
from .rosters import Rosters
from .exceptions import *
from gui.frames.progress_frame import ProgressFrame


def format_name(last: str) -> str:
    return last.strip().upper()


def format_course(course: str) -> str:
    if '-' in course:
        course = course.replace('-', ' ')
    return course.upper()


def get_week(date) -> int:
    start_week = datetime.date(2020, 6, 8).isocalendar()[1]
    week = date.week - start_week
    return week if week >= 0 else 0


# TODO: Validate excel file formatting
def find_student_in_sheet(last: str, _id: str, sheet: pd.DataFrame) -> int:
    last = format_name(last)

    # 1. Search by _id in current course sheet
    row = sheet.loc[sheet['ID'] == _id]

    if not row.empty:
        print(f'SUCCESS: Student found by ID: {_id}\n')
        return row.index[0]
    print('\tUnable to find student by ID in course sheet.')

    # 2. Search by last name in current course sheet
    row = sheet.loc[sheet['Name'].str.upper().str.contains(last)]

    if not row.empty:
        print(f'SUCCESS: Student found by last name: {last}\n')
        return row.index[0]
    print(f'\tUnable to find student by last name in course sheet: {last}')
    print('\n')


class Attendance:
    def __init__(self, responses_path: str, rosters_path: str, output_path: str, progress_frame: ProgressFrame):
        self.progress_frame = progress_frame

        if not responses_path:
            raise ResponsesPathError('Required')
        if not rosters_path:
            raise RostersPathError('Required')
        if not output_path:
            raise OutputPathError('Required')

        try:
            self.responses = Responses(responses_path)
        except OSError as e:
            raise ResponsesError(e.strerror)

        try:
            self.rosters = Rosters(rosters_path)
        except OSError as e:
            raise RostersError(e.strerror)

        self.output_path = output_path

    def parse_response(self, response: pd.Series):
        date, last, _id, course = response
        course = format_course(course)

        print(f'Searching for: {last, _id, course}')

        if course in self.rosters.workbook:
            print(f'\tCourse found in attendance workbook: {course}')
            sheet = self.rosters.workbook[course]

            row_i = find_student_in_sheet(last, _id, sheet)

            # Student found in current sheet
            if row_i is not None:
                # Ignore first 2 columns [ID, Name]
                col_i = 2 + get_week(date)

                # Increment week in student row in corresponding course sheet
                sheet.iat[row_i, col_i] += 1

            # Unable to find student in sheet, search other sheets
            else:
                print(f'\tSearching for student "{last}" in other sheets...')
                # TODO: This would be easier if I had the times for each session - can't assume same student in different
                #  course because they could be in multiple sessions

        else:
            print(f'\tUnable to find course "{course}" in attendance workbook.')
            # TODO: Find most probable course student belongs to

        print()

        # Update progress bar
        self.progress_frame.update_progress_bar()

    def run(self) -> bool:
        self.responses.workbook.apply(self.parse_response, axis=1)

        with pd.ExcelWriter(self.output_path, engine='xlsxwriter') as writer:
            for course, sheet in self.rosters.workbook.items():
                sheet.to_excel(writer, sheet_name=course, index=False)

        return True
