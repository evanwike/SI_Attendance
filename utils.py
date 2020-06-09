import os
import subprocess
import sys
import datetime


def format_name(last: str) -> str:
    return last.strip().upper()


def format_course(course: str) -> str:
    if '-' in course:
        course = course.replace('-', ' ')
    return course.upper()


def get_week(date) -> int:
    start_week = datetime.date(2020, 6, 8).isocalendar()[1]
    week = date.week - start_week
    return week if week >= 0 else 0


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, filename])
