import os
import random
import webbrowser
from dataclasses import dataclass

from utils import SECONDS_IN, File, Time, TimeFormat


@dataclass
class CalendarEvent:
    title: str
    ut_start: int
    t_duration: int

    TIME_FORMAT = TimeFormat('%Y%m%dT%H%M%S')
    EVENTS_PATH = os.path.join(os.environ['DIR_DESKTOP'], 'events.txt')
    MAX_EVENTS = 7

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
        webbrowser.open(self.url)

    @staticmethod
    def get_events() -> list[str]:
        lines = File(CalendarEvent.EVENTS_PATH).read_lines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line and not line.startswith('#')]
        return lines

    @staticmethod
    def get_time_slots() -> list[tuple[int, int]]:
        return [
            (8, 2),
            (10, 2),
            (13, 2),
            (15, 2),
            (18, 2),
        ]

    @staticmethod
    def ut_today_midnight() -> int:
        return (
            int(Time.now().ut / SECONDS_IN.DAY) * SECONDS_IN.DAY
            - 5.5 * SECONDS_IN.HOUR
        )

    @staticmethod
    def build_random_day():
        ut_now = Time.now().ut
        ut = CalendarEvent.ut_today_midnight()
        topics = CalendarEvent.get_events()
        i_day = 0
        n_events = 0
        while True:
            for time_slot in CalendarEvent.get_time_slots():
                title = random.choice(topics)
                h_start, h_duration = time_slot
                ut_start = (
                    ut + h_start * SECONDS_IN.HOUR + i_day * SECONDS_IN.DAY
                )
                t_duration = h_duration * SECONDS_IN.HOUR

                if ut_start < ut_now:
                    continue

                event = CalendarEvent(title, ut_start, t_duration)
                event.open()
                n_events += 1

                if n_events >= CalendarEvent.MAX_EVENTS:
                    break

            if n_events >= CalendarEvent.MAX_EVENTS:
                break


if __name__ == '__main__':
    CalendarEvent.build_random_day()
