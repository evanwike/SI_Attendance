import pandas as pd
import datetime
import logging
import xlsxwriter

logging.basicConfig(filename='errors.log', level=logging.DEBUG)

# TODO: Allow for dynamic file names
RESPONSE_FILE = 'Responses.xlsx'
ATTENDANCE_FILE = 'Attendance_S20.xlsx'

RESPONSE_SHEET = pd.read_excel(RESPONSE_FILE, usecols='C,F:H', names=['Date', 'Last', 'ID', 'Course'], dtype={'ID': str})
# TODO: Fix to work with 8 or 16 week semesters
ATTENDANCE_WBK = pd.read_excel(ATTENDANCE_FILE, sheet_name=None, usecols='A:K', dtype={'ID': str})
ATTENDANCE_WBK = {course: sheet.fillna(0) for (course, sheet) in ATTENDANCE_WBK.items()}


def format_name(last: str) -> str:
    return last.strip().upper()


def format_course(course: str) -> str:
    if '-' in course:
        course = course.replace('-', ' ')
    return course.upper()


def get_week(date) -> int:
    start_week = datetime.date(2020, 6, 8).isocalendar()[1]
    return date.week - start_week


def find_student_in_sheet(last: str, ID: str, course: str):
    sheet = ATTENDANCE_WBK[course]
    last = format_name(last)

    # 1. Search by ID in current course sheet
    row = sheet.loc[sheet['ID'] == ID]

    if not row.empty:
        print(f'SUCCESS: Student found by ID: {ID}\n')
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
    date, last, ID, course = response
    course = format_course(course)

    print(f'Searching for: {last, ID, course}')

    if course in ATTENDANCE_WBK:
        print(f'\tCourse found in attendance workbook: {course}')

        row_index = find_student_in_sheet(last, ID, course)

        # Student found in current sheet
        if row_index is not None:
            week = 2 + get_week(date)

            # Increment week in student row in corresponding course sheet
            ATTENDANCE_WBK[course].iat[row_index, week] += 1

        # Unable to find student in sheet, search other sheets
        else:
            print(f'\tSearching for student "{last}" in other sheets...')
            # TODO: This would be easier if I had the times for each session - can't assume same student in different
            #  course because they could be in multiple sessions

    else:
        print(f'\tUnable to find course "{course}" in attendance workbook.')
        # TODO: Find most probably course student belongs to

    print()


def main():
    RESPONSE_SHEET.apply(parse, axis=1)

    with pd.ExcelWriter('Attendance_S20_TABULATED.xlsx', engine='xlsxwriter') as writer:
        for course, sheet in ATTENDANCE_WBK.items():
            sheet.to_excel(writer, sheet_name=course, index=False)


main()
