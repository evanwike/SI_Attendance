import pandas as pd


# Microsoft Teams Attendance Form Responses
class Responses:
    def __init__(self, path):
        self.path = path
        # TODO: Possibly add support to dynamically choose columns
        try:
            self.workbook = pd.read_excel(
                path,
                usecols='C,F:H',
                names=['Date', 'Last', 'ID', 'Course'],
                dtype={'ID': str})
        except OSError as e:
            raise e
        except Exception as e:
            print(e)

    def get_num_responses(self) -> int:
        return len(self.workbook.index)
