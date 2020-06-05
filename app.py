import pandas as pd
import datetime
import logging
# import difflib
from gui.gui import GUI


logging.basicConfig(filename='errors.log', level=logging.DEBUG)

# TODO: Allow for dynamic file names
PATH = 'data/'
EXT = '.xlsx'
RESPONSE_FILE = 'Responses'
ATTENDANCE_FILE = 'Attendance_S20'
OUT_FILE = PATH + 'out/' + ATTENDANCE_FILE + '_TABULATED' + EXT

RESPONSE_SHEET = pd.read_excel(
    PATH + RESPONSE_FILE + EXT,
    usecols='C,F:H',
    names=['Date', 'Last', 'ID', 'Course'],
    dtype={'ID': str})

# TODO: Fix to work with 8 or 16 week semesters
# TODO: Do we want this to mutate current attendance workbook, or create a new one?
ATTENDANCE_WBK = {course: sheet.fillna(0) for (course, sheet) in
                  pd.read_excel(
                      PATH + ATTENDANCE_FILE + EXT,
                      sheet_name=None,
                      usecols='A:K',
                      dtype={'ID': str}
                  ).items()}


# ATTENDANCE_WBK = {course: sheet.fillna(0) for (course, sheet) in ATTENDANCE_WBK.items()}


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


def find_student_in_sheet(last: str, _id: str, course: str):
    sheet = ATTENDANCE_WBK[course]
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


def parse(response):
    date, last, _id, course = response
    course = format_course(course)

    print(f'Searching for: {last, _id, course}')

    if course in ATTENDANCE_WBK:
        print(f'\tCourse found in attendance workbook: {course}')

        row_i = find_student_in_sheet(last, _id, course)

        # Student found in current sheet
        if row_i is not None:
            # Ignore first 2 columns [ID, Name]
            col_i = 2 + get_week(date)

            # Increment week in student row in corresponding course sheet
            ATTENDANCE_WBK[course].iat[row_i, col_i] += 1

        # Unable to find student in sheet, search other sheets
        else:
            print(f'\tSearching for student "{last}" in other sheets...')
            # TODO: This would be easier if I had the times for each session - can't assume same student in different
            #  course because they could be in multiple sessions

    else:
        print(f'\tUnable to find course "{course}" in attendance workbook.')
        # TODO: Find most probable course student belongs to

    print()


def main():
    # RESPONSE_SHEET.apply(parse, axis=1)
    #
    # with pd.ExcelWriter(OUT_FILE, engine='xlsxwriter') as writer:
    #     for course, sheet in ATTENDANCE_WBK.items():
    #         sheet.to_excel(writer, sheet_name=course, index=False)

    gui = GUI()
    gui.run()


main()
