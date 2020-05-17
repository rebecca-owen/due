#!/usr/bin/env python3
"""
due.py
Python3 script for todo.txt add-on
Created by Rebecca Morgan 2017-03-10
Copyright (c) 2017 Rebecca Morgan. Licensed under MIT.

Edits by Steve Winslow 2017-06-25
Edits copyright (c) 2017 Steve Winslow. Licensed under MIT.
"""

import os
import sys
import math
from datetime import datetime, timedelta
import re


def task_print(task):
    """
    Print the task string, coloring according to priority if set.

    Argument: task
        Task string
    """
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


def main(todo_file, future_days=1):
    """
    Print task information, sorted by due date.

    Argument: todo_file
        The path to the todo.txt file

    Argument: future_days (default: 1)
        Number of days in the future to consider due dates to print.
        Default behaviour includes tasks due tomorrow - this can be
        overriden by passing 0.
    """
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
            match = re.findall(r"%s:(\d{4}-\d{2}-\d{2})" % key, task)

            if match:
                date = datetime.strptime(match[0], "%Y-%m-%d").date()
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

    # Print to console
    if len(overdue) > 0:
        print("===================================")
        print("Overdue tasks:")
        print("===================================")
        for task in overdue:
            task_print(task)
    if len(due_today) > 0:
        print("\n===================================")
        print("Tasks due today:")
        print("===================================")
        for task in due_today:
            task_print(task)
    if len(due_tmr) > 0 and future_days >= 1:
        print("\n===================================")
        print("Tasks due tomorrow:")
        print("===================================")
        for task in due_tmr:
            task_print(task)
    if len(due_future) > 0:
        print("\n===================================")
        print(f"Tasks due in the next {str(future_days)} days:")
        print("===================================")
        for task in due_future:
            task_print(task)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: due.py [TODO_FILE] <future_days>")
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        if len(sys.argv) == 3:
            if str.isdigit(sys.argv[2]):
                main(sys.argv[1], int(sys.argv[2]))
            else:
                print(f"Error: future_days argument '{sys.argv[2]}' is not an integer")
                sys.exit(1)
        else:
            main(sys.argv[1])
    else:
        print(f"Error: {sys.argv[1]} is not a file")
        sys.exit(1)
