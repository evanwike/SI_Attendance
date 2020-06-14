import pandas as pd


# Microsoft Teams Attendance Form Responses
# TODO: Possibly add support to dynamically choose columns
class Responses:
    def __init__(self, path):
        self.path = path

        try:
            self.workbook = pd.read_excel(
                path,
                usecols='C,E:G',
                names=['Date', 'Last', 'ID', 'Course'],
                dtype={'ID': str})
        except OSError as e:
            raise e
        except Exception as e:
            print(e)

    def get_num_responses(self) -> int:
        return len(self.workbook.index)
