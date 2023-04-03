import calendar
import sys

def restmonth(year, month):

    cal = calendar.monthcalendar(year, month)

    headerHeader = calendar.month(2023,4).split("\n")[0].strip()
    table_header = "+---+---+---+---+---+---+---+\n|Mon|Tue|Wed|Thu|Fri|Sat|Sun|"

    table_rows = ""
    for week in cal:
        row = "|"
        for day in week:
            if day == 0:
                row += "   |"
            else:
                if day < 10:
                    row += f" {day} |"
                else:
                    row += f" {day}|"
        table_rows += f"+---+---+---+---+---+---+---+\n{row}\n"

    table = f"{table_header}\n{table_rows}+---+---+---+---+---+---+---+"

    with open("calendar.rst", "w") as file:
        file.write(table)


if __name__ == "__main__":
    restmonth(sys.argv[0], sys.argv[1])