"""Shows the commit logs.

The command takes options applicable to the git rev-list command to control
what is shown and how, and options applicable to the git diff-* commands to
control how the changes each commit introduces are shown.
"""

from os import listdir
import datetime
from .tools import get_full_path, read_file


def get_month(number):
    """
    get_month(number)   ->  return month as string.

    Required argument:
        number  --  month in numbers.
    """
    switcher = {
        '01': 'Jan',
        '02': 'Feb',
        '03': 'Mar',
        '04': 'Apr',
        '05': 'May',
        '06': 'Jun',
        '07': 'Jul',
        '08': 'Aug',
        '09': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'
    }
    month = switcher.get(number)
    return month


def get_week_day(number):
    """
    get_week_day(number) -> return weekday.

    Required argument:
        number  -- a 14 digist numbers.
    """
    year = int(number[:4])
    month = int(number[4:6])
    day = int(number[6:8])
    print(year, month, day)
    date = datetime.datetime(year, month, day).weekday()
    week = {
        0: 'Mon',
        1: 'Tue',
        3: 'Wed',
        4: 'Thu',
        5: 'Fri',
        6: 'Sat',
        7: 'Sun'
    }
    return week.get(date)


def execute_log(repo):
    """
    execute_log(repo)   -> Show the commit logs.

    Required argument:
        repo    --  path of repository.
    """
    directories = listdir(repo + "/.lgit/commits")
    directory.sort(reverse=True)
    for directory in directories:
        print("commit", directory)
        path = get_full_path(repo + "/.lgit/commits" + directoy)
        contents = read_file(path).split('\n')
        while '' in content:
            content.remove('')
        print("Author:", contents[0])
        print("Date:", get_week_day(contents[1]),
              get_month(contents[1][4:6]), contents[1][6:8],
              contents[1][8:10] + ":" + contents[1][10:12] +
              ":" + contents[1][12:14], contents[1][:4] + '\n')
        print('\t' + content[2] + '\n\n')
    return 0
