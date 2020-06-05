import pandas as pd
import datetime

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


def find_student(last: str, ID: str, course: str):
    print(f'Searching for: {last, ID, course}')

    last = format_name(last)
    course = format_course(course)

    # Found course in attendance book
    if course in ATTENDANCE_WBK:
        print(f'\tFound course {course} in attendance book.')
        df = ATTENDANCE_WBK[course]

        # 1. Search by ID in current course sheet
        row = df.loc[df['ID'] == ID]

        if not row.empty:
            print(f'SUCCESS: Student found by ID {ID}.\n')
            return course, row.index[0]
        print('\tUnable to find student by ID in course sheet.')

        # 2. Search by last name in current course sheet
        row = df.loc[df['Name'].str.upper().str.contains(last)]

        if not row.empty:
            print(f'SUCCESS: Student found by last name.\n')
            return course, row.index[0]
        print(f'\tUnable to find student by last name in course sheet: {last}')

    # Unable to find course in attendance book
    else:
        print(f'\tUnable to find course "{course}" in attendance book.')
        print(f'\tSearching for student "{last}" in other sheets...')

        # 3. Search other course sheets
    print()


def get_week(date) -> int:
    start_week = datetime.date(2020, 6, 8).isocalendar()[1]
    return date.week - start_week


def parse(response):
    date, last, ID, course = response
    student = find_student(last, ID, course)

    if student is not None:
        course, row_ind = student
        # Ignore first 2 columns
        week = 2 + get_week(date)

        # Increment week in student row in corresponding course sheet
        ATTENDANCE_WBK[course].iat[row_ind, week] += 1


def main():
    RESPONSE_SHEET.apply(parse, axis=1)

    with pd.ExcelWriter('Attendance_S20_TABULATED.xlsx', engine='xlsxwriter') as writer:
        for course, sheet in ATTENDANCE_WBK.items():
            sheet.to_excel(writer, sheet_name=course, index=False)


main()
