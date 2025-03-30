from cal import MonthCalendar, WeekCalendar

if __name__ == "__main__":

    year = 2025
    for month in [5]:
        MonthCalendar(year, month).draw()

    for month, day in [[3, 31], [4,7]]:
        WeekCalendar(year, month, day).draw()
