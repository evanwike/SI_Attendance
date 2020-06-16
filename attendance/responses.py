import pandas as pd
from exceptions import ResponsesError


# Microsoft Teams Attendance Form Responses
class Responses:
    def __init__(self, path):
        self.path = path

        try:
            self.df = pd.read_excel(
                path,
                usecols='C,E:G',
                names=['Date', 'Last', 'ID', 'Course'],
                dtype={'ID': str})
        except OSError as e:
            raise ResponsesError(e.strerror)
        except Exception as e:
            raise e

    def get_num_responses(self) -> int:
        return len(self.df.index)
