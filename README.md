# due
A [todo.txt](http://todotxt.com/) plugin to display your due and overdue tasks using Python 2/3.

In order to use this plugin, tasks must be added with due dates in the format:
```
due:YYYY-MM-DD
```

# Installation

In order to install actions in sub-directories of the add-on directory, please use todo.txt [version 2.10](https://github.com/ginatrapani/todo.txt-cli/releases/tag/v2.10). Following [Installing Add-ons](https://github.com/ginatrapani/todo.txt-cli/wiki/Creating-and-Installing-Add-ons), first `cd`
into your `.todo.actions.d` directory. The default location is within `$HOME`:
```
cd ~/.todo.actions.d
```

Clone this repository:
```
git clone https://github.com/rebeccamorgan/due.git
```

Now make the `due` shell script executable:
```
chmod +x due
```

# Usage
Default behaviour displays tasks that are overdue, due today or due tomorrow:
```
todo.sh due
```

An optional argument of an integer n will also print the tasks due in the next n days (not including today). For example, to also see tasks due in the next week:
```
todo.sh due 7
```

# Compatibility
Tested with todo.txt_cli-2.9 on macOS 10.12.3 and todo.txt_cli-2.10 on Ubuntu. 

