import webbrowser
from dataclasses import dataclass

from utils import Log, Time, TimeFormat

log = Log('CalendarEvent')


@dataclass
class CalendarEvent:
    title: str
    ut_start: int
    t_duration: int

    TIME_FORMAT = TimeFormat('%Y%m%dT%H%M%S')

    @staticmethod
    def format_time(ut: int):
        return CalendarEvent.TIME_FORMAT.stringify(Time(ut))

    @property
    def time_start(self) -> str:
        return CalendarEvent.format_time(self.ut_start)

    @property
    def time_end(self) -> str:
        return CalendarEvent.format_time(self.ut_start + self.t_duration)

    @property
    def url(self) -> str:
        return (
            "https://calendar.google.com/calendar/u/0/r/eventedit"
            + f"?text={self.title}&dates={self.time_start}/{self.time_end}"
        )

    def open(self):
        log.info(self.url)
        webbrowser.open(self.url)
