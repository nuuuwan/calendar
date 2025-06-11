from cal import MonthCalendar, WeekCalendar, YearCalendar

if __name__ == "__main__":

    year = 2025

    # YearCalendar(year).draw()
    # YearCalendar(2026).draw()

    for month in [9]:
        MonthCalendar(year, month).draw()

    for month, day in [[6, 16], [6, 23], [6, 30]]:
        WeekCalendar(year, month, day).draw()
