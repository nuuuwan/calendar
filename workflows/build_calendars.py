from cal import MonthCalendar, WeekCalendar

if __name__ == "__main__":

    year = 2025
    for month in [2, 3, 4]:
        MonthCalendar(year, month).draw()

    for month, day in [[2, 10], [2, 17], [2, 24]]:
        WeekCalendar(year, month, day).draw()
