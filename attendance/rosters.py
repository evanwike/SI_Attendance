import pandas as pd


# Section Rosters
class Rosters:
    # TODO: Validate Excel file formatting
    def __init__(self, path):
        self.path = path

        weeks = 8
        names = ['ID', 'Name'] + [f'Week {i+1}' for i in range(weeks)] + ['Total', '', '', '']

        try:
            # FIXME: Dynamic columns to allow for 8 or 16 week
            self.workbook = pd.read_excel(
                path,
                sheet_name=None,
                usecols='A:N',
                dtype={'ID': str},
                names=names
            )
        except OSError as e:
            raise e
        except Exception as e:
            print(e)

    def search_sheet_by_id(self, _id: str, course: str) -> int:
        sheet = self.workbook[course]
        row = sheet.loc[sheet['ID'] == _id]

        if not row.empty:
            print(f'SUCCESS: Student found by ID: {_id}\n')
            return row.index[0]
        print('\tUnable to find student by ID in course sheet.')
        return -1

    def search_sheet_by_last_name(self, last: str, course: str) -> int:
        sheet = self.workbook[course]
        row = sheet.loc[sheet['Name'].str.upper().str.contains(last)]

        if not row.empty:
            print(f'SUCCESS: Student found by last name: {last}\n')
            return row.index[0]
        print(f'\tUnable to find student by last name in course sheet: {last}\n')
        return -1

    def find_student_in_sheet(self, _id: str, last: str, course: str):
        # 1. Search by _id in current course sheet
        row = self.search_sheet_by_id(_id, course)
        if row != -1:
            return row
        # 2. Search by last name in current course sheet
        row = self.search_sheet_by_last_name(last, course)
        if row != -1:
            return row

    def increment_student(self, course: str, row: int, col: int) -> None:
        sheet = self.workbook[course]
        val = sheet.iat[row, col]
        sheet.iat[row, col] = 1 if type(val) != int else val + 1
        # sheet.iat[row, col] =
        # a = sheet.iat[row, col]
        # print(type(a), a)
        # sheet.iat[row, col] += 1
