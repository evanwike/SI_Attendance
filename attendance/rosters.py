import pandas as pd


class Rosters:
    def __init__(self, path):
        self.path = path

        try:
            self.workbook = {
                course: sheet.fillna(0) for (course, sheet) in
                pd.read_excel(
                    path,
                    sheet_name=None,
                    usecols='A:K',
                    dtype={'ID': str}
                ).items()}
        except OSError as e:
            raise e
        except Exception as e:
            print(e)
