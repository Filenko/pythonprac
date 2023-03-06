import cmd
import shlex
from calendar import TextCalendar

class ech(cmd.Cmd):
    prompt = "> "


    def do_month(self, arg):
        """month [year] [month] -- Print a month’s calendar"""
        args = shlex.split(arg)
        if len(args) != 2:
            return
        else:
            cal = TextCalendar()
            print(cal.prmonth(theyear=int(args[0]), themonth=int(args[1])))

    def do_year(self, arg):
        """year [year] [month] -- Print the calendar for an entire year"""
        args = shlex.split(arg)
        if len(args) != 1:
            return
        else:
            cal = TextCalendar()
            print(cal.pryear(theyear=int(args[0])))

    def complete_month(self, prefix, line, start, end):
        return [str(m) for m in range(1, 13) if str(m).startswith(prefix)]

    def do_quit(self):
        return 1


ech().cmdloop()

