import pandas as pd
import logging
import utils
from .responses import Responses
from .rosters import Rosters
from .exceptions import *
from gui.frames.progress_frame import ProgressFrame


class Attendance:
    def __init__(self, responses_path: str, rosters_path: str, progress_frame: ProgressFrame):
        self.progress_frame = progress_frame

        if not responses_path:
            raise ResponsesPathError('Required')
        if not rosters_path:
            raise RostersPathError('Required')

        try:
            self.responses = Responses(responses_path)
        except OSError as e:
            raise ResponsesError(e.strerror)

        try:
            self.rosters = Rosters(rosters_path)
        except OSError as e:
            raise RostersError(e.strerror)

    def parse_response(self, response: pd.Series):
        date, last, _id, course = response
        course = utils.format_course(course)

        print(f'Searching for: {last, _id, course}')

        if course in self.rosters.workbook:
            print(f'\tCourse found in attendance workbook: {course}')

            # 1. Search by _id in current course sheet
            row = self.rosters.search_sheet_by_id(_id, course)

            if row is not None:
                # Found student in current sheet
                # TODO: Get week as input
                # Ignore headers, OpenPyXl indexing starts from 1
                row += 2
                # Ignore first 2 columns [ID, Name], OpenPyXl indexing starts from 1
                col = 3 + utils.get_week(date)
                self.rosters.increment_student(course, row, col)
            else:
                # Unable to find student in sheet, search other sheets
                print(f'\tSearching for student "{last}" in other sheets...')
                # TODO: This would be easier if I had the times for each session - can't assume same student in
                #  different course because they could be in multiple sessions
        else:
            print(f'\tUnable to find course "{course}" in attendance workbook.')
            # TODO: Find most probable course student belongs to
        print()

        # Update progress bar
        self.progress_frame.update_progress_bar()

    def run(self) -> bool:
        # TODO: Rework how it writes to Excel
        # Move writing to parse_response
        self.responses.workbook.apply(self.parse_response, axis=1)
        self.rosters.write_workbook.save()
        return True
        # with pd.ExcelWriter(self.rosters.path, engine='xlsxwriter') as writer:
        #     for course, sheet in self.rosters.workbook.items():
        #         sheet.to_excel(writer, sheet_name=course, index=False)
