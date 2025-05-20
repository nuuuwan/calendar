import calendar

from utils import Log, Time, TimeDelta, TimeFormat, TimeUnit, _

from cal.AbstractCalendar import AbstractCalendar
from cal.HOLIDAYS import HOLIDAYS

log = Log("WeekCalendar")


class WeekCalendar(AbstractCalendar):

    N_X = 7
    N_Y = 8
    BOX_WIDTH = AbstractCalendar.DISPLAY_WIDTH / N_X
    BOX_HEIGHT = AbstractCalendar.DISPLAY_HEIGHT / N_Y

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    @property
    def time_start(self):
        return self.time

    @property
    def time_end(self):
        return self.time_start + TimeDelta(TimeUnit.SECONDS_IN.DAY * 6)

    @property
    def time_format(self):
        return TimeFormat("%Y-%m-%d")

    @property
    def week_num(self):
        # HACK! Should be implemented in Time
        ut = self.time_start.ut
        year = (int)(TimeFormat("%Y").stringify(self.time_start))
        ut0 = TimeFormat("%Y").parse(f"{year}").ut
        week_num = int(((ut - ut0)) // TimeUnit.SECONDS_IN.DAY // 7 + 1)
        return week_num

    @property
    def title(self):
        date_start = self.time_format.stringify(self.time_start)
        date_end = self.time_format.stringify(self.time_end)

        return f"{date_start} to {date_end} (Week {self.week_num})"

    def render_title(self):
        return _(
            "text",
            self.title,
            self.point(0.5, -0.07)
            | dict(
                font_size=30,
                text_anchor="middle",
            ),
        )

    def render_box_background(self, x, y, holiday_text):
        return _(
            "rect",
            None,
            dict(
                fill="#eee" if holiday_text else "#fff",
                stroke="black",
                width=self.BOX_WIDTH,
                height=self.BOX_HEIGHT,
            )
            | self.point(x / self.N_X, y / self.N_Y),
        )

    def render_box_day(self, x, y, day):
        return _(
            "text",
            f"{day}" if day != 0 else "",
            dict(
                fill="black",
                stroke="none",
                font_size=15,
                width=self.BOX_WIDTH,
                height=self.BOX_HEIGHT,
            )
            | self.point(
                (x + 0.1) / self.N_X,
                (y + 0.2) / self.N_Y,
            ),
        )

    def render_box_holiday(self, x, y, holiday_text):
        return _(
            "text",
            holiday_text,
            dict(
                fill="#888",
                stroke="none",
                font_size=12,
                width=self.BOX_WIDTH,
                height=self.BOX_HEIGHT,
            )
            | self.point(
                (x + 0.1) / self.N_X,
                (y + 0.8) / self.N_Y,
            ),
        )

    def render_box(self, x, y, day):
        if not day:
            return None

        holiday_text = (
            HOLIDAYS.get(day.year, {}).get(day.month, {}).get(day.day, "")
        )

        return _(
            "g",
            [
                self.render_box_background(x, y, holiday_text),
                self.render_box_day(x, y, day.day) if (y == 0) else None,
                (
                    self.render_box_holiday(x, y, holiday_text)
                    if (y == self.N_Y - 1)
                    else None
                ),
            ],
        )

    def render_box_grid(self):
        box_list = []
        from datetime import datetime, timedelta

        start_date = datetime(self.year, self.month, self.day)
        days = [start_date + timedelta(days=i) for i in range(7)]

        for i, day in enumerate(days):
            x = i % self.N_X
            for y in range(self.N_Y):
                box = self.render_box(x, y, day)
                box_list.append(box)
        return box_list

    def render_header_box_row(self):

        header_box_row = []
        for y in [-0.015, 1.025]:
            for x, day_name in enumerate(list(calendar.day_abbr)):
                header_box = _(
                    "g",
                    [
                        _(
                            "text",
                            day_name,
                            dict(
                                fill="black",
                                stroke="none",
                                text_anchor="middle",
                                dominant_baseline="middle",
                                font_size=20,
                                width=self.DISPLAY_WIDTH / 7,
                                height=self.DISPLAY_HEIGHT / 6,
                            )
                            | self.point(
                                (x + 0.5) / self.N_X,
                                (y),
                            ),
                        ),
                    ],
                )
                header_box_row.append(header_box)

        return header_box_row

    def render_header_box_col(self):

        header_box_col = []
        time_format = TimeFormat("%I%p")
        for x in [-0.035, 1.035]:
            for y in range(self.N_Y):
                time_start = Time(
                    self.time.ut + (y * 2 + 6) * TimeUnit.SECONDS_IN.HOUR
                )
                time_end = time_start + TimeDelta(
                    TimeUnit.SECONDS_IN.HOUR * 2
                )
                time_str = ""
                if 0 < y < self.N_Y - 1:
                    time_str = (
                        time_format.stringify(time_start)
                        + " - "
                        + time_format.stringify(time_end)
                    )
                header_box = _(
                    "g",
                    [
                        _(
                            "text",
                            time_str,
                            dict(
                                fill="black",
                                stroke="none",
                                text_anchor="middle",
                                font_size=10,
                                width=self.DISPLAY_WIDTH / 7,
                                height=self.DISPLAY_HEIGHT / 6,
                            )
                            | self.point(
                                x,
                                (y + 0.5) / self.N_Y,
                            ),
                        ),
                    ],
                )
                header_box_col.append(header_box)

        return header_box_col

    def render(self):
        return _(
            "svg",
            self.render_header_box_row()
            + self.render_header_box_col()
            + self.render_box_grid()
            + [self.render_title()],
            dict(
                width=self.WIDTH,
                height=self.HEIGHT,
                font_family="Ubuntu Mono",
            ),
        )
