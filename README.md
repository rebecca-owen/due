# due
A [todo.txt](http://todotxt.com/) plugin to display your due and overdue tasks using Python 2.

In order to use this plugin, tasks must be added with due dates in the format:
```
due:YYYY-MM-DD
```

# Installation

Following [Installing Add-ons](https://github.com/ginatrapani/todo.txt-cli/wiki/Creating-and-Installing-Add-ons), first `cd`
into your `.todo.actions.d` directory. The default location is within `$HOME`:
```
cd ~/.todo.actions.d
```

Clone this directory into a new directory `due`:
```
git clone https://github.com/rebeccamorgan/due.git due
```

Now `cd` into this new `due` directory and make the shell script executable:
```
chmod +x due
```

# Usage
Default behaviour displays tasks that are overdue or due today:
```
todo.sh due
```

An optional argument of an integer n will also print the tasks due in the next n days (not including today). For example, to also see tasks due in the next week:
```
todo.sh due 7
```

# Compatibility
Tested with todo.txt_cli-2.9 on macOS 10.12.3

