#!/usr/bin/env python
"""
due.py
Python 2 script for todo.txt add-on
Created by Rebecca Morgan 2017-03-10
Copyright (c) 2017 Rebecca Morgan. All rights reserved.

Edits by Steve Winslow 2017-06-25
Edits copyright (c) 2017 Steve Winslow. Licensed under MIT.
"""

import os
import sys
from datetime import datetime, timedelta
import re

def main(todo_file, future_days = 0):
    # Prepare lists to store tasks
    overdue = list()
    due_today = list()
    due_future = list()

    # Open todo.txt file
    with open(todo_file, 'r') as f:
        content = f.readlines()
        date = datetime.today()

        # Loop through content and look for due dates, assuming the key due: is used and standard date format
        for i, task in enumerate(content):
            match = re.search(r'due:\d{4}-\d{2}-\d{2}', task)

            if match is not None:
                date = datetime.strptime(match.group()[4:], '%Y-%m-%d').date()

                # Add matching tasks to list with line number
                if date < datetime.today().date():
                    overdue.append(str(i+1).zfill(2) + " " + task)
                elif date == datetime.today().date():
                    due_today.append(str(i+1).zfill(2) + " " + task)
                elif date < datetime.today().date() + timedelta(days=future_days+1):
                    due_future.append(str(i+1).zfill(2) + " " + task)

    # Print to console
    if len(overdue) > 0:
        print "==============================="
        print "Overdue tasks:"
        print "==============================="
        for task in overdue:
            print task,
    if len(due_today) > 0:
        print "==============================="
        print "Tasks due today:"
        print "==============================="
        for task in due_today:
            print task,
    if len(due_future) > 0:
        print "==============================="
        print "Tasks due in the next " + str(future_days) + " days:"
        print "==============================="
        for task in due_future:
            print task,

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Usage: due.py [TODO_FILE] <future_days>"
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        if len(sys.argv) is 3:
            main(sys.argv[1], int(sys.argv[2]))
        else:
            main(sys.argv[1])
    else:
        print "Error: %s is not a file" % sys.argv[1]
        sys.exit(1)
