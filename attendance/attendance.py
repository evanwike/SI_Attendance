import pandas as pd


# Section Rosters
class Rosters:
    # TODO: Validate Excel file formatting
    def __init__(self, path):
        self.path = path

        try:
            self.workbook = pd.read_excel(
                path,
                sheet_name=None,
                dtype={'ID': str})
        except OSError as e:
            raise e

        # Detect upper bound of week
        i = 0
        while f'Week {i + 1}' in next(iter(self.workbook.values())):
            i += 1
        self.week_bound = i

    def search_sheet_by_id(self, _id: str, course: str) -> int:
        sheet = self.workbook[course]
        row = sheet.loc[sheet['ID'] == _id]

        if not row.empty:
            print('SUCCESS')
            return row.index[0]
        print('FAILURE')
        return -1

    def search_sheet_by_last_name(self, last: str, course: str) -> int:
        sheet = self.workbook[course]
        row = sheet.loc[sheet['Name'].str.upper().str.startswith(last.upper())]

        if not row.empty:
            print('SUCCESS')
            return row.index[0]
        print('FAILURE')
        return -1

    def find_student_in_sheet(self, _id: str, last: str, course: str):
        # 1. Search by _id in current course sheet
        print('\tSearching by ID...', end=' ')
        row = self.search_sheet_by_id(_id, course)
        if row != -1:
            return row
        # 2. Search by last name in current course sheet
        print('\tSearching by Last Name...', end=' ')
        row = self.search_sheet_by_last_name(last, course)
        if row != -1:
            return row

    def increment_student(self, course: str, row: int, col: int) -> None:
        sheet = self.workbook[course]
        val = sheet.iat[row, col]
        sheet.iat[row, col] = 1 if pd.isna(val) else val + 1

    def get_week_bound(self) -> int:
        return self.week_bound
