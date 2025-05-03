from cal import MonthCalendar, WeekCalendar

if __name__ == "__main__":

    year = 2025
    for month in [6, 7, 8]:
        MonthCalendar(year, month).draw()

    for month, day in [[5, 5], [5, 12], [5, 19]]:
        WeekCalendar(year, month, day).draw()
