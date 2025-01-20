from cal import WeekCalendar

if __name__ == "__main__":

    # MonthCalendar(2025, 3).draw()

    year = 2025
    for month, day in [[1, 20], [1, 27], [2, 3]]:
        WeekCalendar(year, month, day).draw()
