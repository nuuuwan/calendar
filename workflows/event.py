import sys

from utils import Time, TimeUnit

from cal import CalendarEvent

if __name__ == '__main__':
    title = sys.argv[1].replace(" ", "+")
    ut_start = Time.now().ut
    t_duration = TimeUnit.SECONDS_IN.HOUR * 2
    CalendarEvent(title, ut_start, t_duration).open()
