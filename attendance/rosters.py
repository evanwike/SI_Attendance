import pandas as pd
from exceptions import RostersError


class Rosters:
    def __init__(self, path: str):
        self.path = path

        try:
            self.workbook = pd.read_excel(
                path,
                sheet_name=None,
                dtype={'ID': str})
        except OSError as e:
            raise RostersError(e.strerror)
        except Exception as e:
            raise e

        # Get # of weeks by checking if Week 9 is among the columns or the first sheet
        self.num_weeks = 8 if 'Week 9' not in next(iter(self.workbook.values())).columns else 16

    def __contains__(self, item):
        return item in self.workbook
