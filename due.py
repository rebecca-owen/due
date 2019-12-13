#!/usr/bin/env python
"""
due.py
Python 2/3 script for todo.txt add-on
Created by Rebecca Morgan 2017-03-10
Copyright (c) 2017 Rebecca Morgan. All rights reserved.

Edits by Steve Winslow 2017-06-25
Edits copyright (c) 2017 Steve Winslow. Licensed under MIT.

Edits by Matias Vidal matias@m01.cl 2019-12-11
Edits copyright (c) 2019 Matias Vidal. Licensed under MIT.
"""

from __future__ import print_function
from __future__ import division

import os
import sys
import math
from datetime import datetime, timedelta
import re


def task_print(task):
    match = re.search(r"\s\(([A-Z])\)\s", task)

    if match is None:
        print(task, end="")
    else:
        pri = match.group(1)
        color = os.getenv("PRI_" + pri)

        if color is None:
            color = os.getenv("PRI_X")

        color = eval('u"' + color[1:] + '"')
        print(color + task + "\033[0m", end="")


def main(todo_file, future_days=0, summary=False):
    # Prepare lists to store tasks
    overdue = list()
    due_today = list()
    due_tmr = list()
    due_future = list()
    tasks_with_date = list()

    # Open todo.txt file
    with open(todo_file, "r") as f:
        content = f.readlines()
        date = datetime.today()

        # Loop through content and look for due dates, assuming standard date format
        key = os.getenv("TODO_TXT_DUE_KEY", "due")

        for i, task in enumerate(content):
            match = re.findall(
                r"(\([A-Z]\))?[A-Za-z0-9+@\s]+%s:(\d{4}-\d{2}-\d{2})" % key, task
            )

            if match:
                date = datetime.strptime(match[0][1], "%Y-%m-%d").date()
                tasks_with_date.append((i, task, date))

        # Sort tasks with a due date: regex by date, then priority
        sorted_tasks = sorted(tasks_with_date, key=lambda tup: (tup[2], tup[1]))
        zero_pad = int(math.log10(len(content))) + 1

        # Append to relevant lists for output
        for task in sorted_tasks:
            # Add matching tasks to list with line number
            if task[2] < datetime.today().date():
                overdue.append(str(task[0] + 1).zfill(zero_pad) + " " + task[1])
            elif task[2] == datetime.today().date():
                due_today.append(str(task[0] + 1).zfill(zero_pad) + " " + task[1])
            elif task[2] == datetime.today().date() + timedelta(days=1):
                due_tmr.append(str(task[0] + 1).zfill(zero_pad) + " " + task[1])
            elif task[2] < datetime.today().date() + timedelta(days=future_days + 1):
                due_future.append(str(task[0] + 1).zfill(zero_pad) + " " + task[1])

    if summary:
        print("Overdue: %i/Today: %i/Tomorrow: %i" % (len(overdue), len(due_today), len(due_tmr)))

    else:
        # Print to console
        if overdue:
            print("===============================")
            print("Overdue tasks: %i" % (len(overdue)))
            print("===============================")
            for task in overdue:
                task_print(task)
        if due_today:
            print("\n===============================")
            print("Tasks due today: %i" % (len(due_today)))
            print("===============================")
            for task in due_today:
                task_print(task)
        if due_tmr:
            print("\n===============================")
            print("Tasks due tomorrow: %i" % (len(due_tmr)))
            print("===============================")
            for task in due_tmr:
                task_print(task)
        if due_future:
            print("\n===============================")
            print("Tasks due in the following %s days: %i" % (str(future_days - 1), len(due_future)))
            print("===============================")
            for task in due_future:
                task_print(task)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: due.py [TODO_FILE] <future_days|summary>")
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        if len(sys.argv) == 3:
            if sys.argv[2].isdigit():
                future_days = int(sys.argv[2])
                summary = False
            elif sys.argv[2].startswith("sum"):
                future_days = 0
                summary = True
            main(sys.argv[1], future_days, summary)
        else:
            main(sys.argv[1])
    else:
        print("Error: %s is not a file" % sys.argv[1])
        sys.exit(1)
