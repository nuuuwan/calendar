import calendar

from utils import Log, TimeFormat, _

from cal.AbstractCalendar import AbstractCalendar
from cal.HOLIDAYS import HOLIDAYS

log = Log("MonthCalendar")


class MonthCalendar(AbstractCalendar):

    N_X = 7
    N_Y = 6
    BOX_WIDTH = AbstractCalendar.DISPLAY_WIDTH / N_X
    BOX_HEIGHT = AbstractCalendar.DISPLAY_HEIGHT / N_Y

    def __init__(self, year, month):
        self.year = year
        self.month = month

    def __str__(self):
        return f"{self.year}-{self.month:02d}"

    @property
    def time_format(self):
        return TimeFormat("%Y-%m")

    def render_title(self):
        return _(
            "text",
            TimeFormat("%Y %B").stringify(self.time),
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
                font_size=20,
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
            HOLIDAYS.get(self.year, {}).get(self.month, {}).get(day, "")
        )
        return _(
            "g",
            [
                self.render_box_background(x, y, holiday_text),
                self.render_box_day(x, y, day),
                self.render_box_holiday(x, y, holiday_text),
            ],
        )

    def render_box_grid(self):
        box_list = []

        cal = calendar.Calendar()
        days = list(cal.itermonthdays(self.year, self.month))

        for i, day in enumerate(days):
            x = i % self.N_X
            y = i // self.N_X
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
                                font_size=20,
                                width=self.DISPLAY_WIDTH / 7,
                                height=self.DISPLAY_HEIGHT / 6,
                            )
                            | self.point(
                                (x + 0.5) / self.N_X,
                                y,
                            ),
                        ),
                    ],
                )
                header_box_row.append(header_box)

        return header_box_row

    def render(self):
        return _(
            "svg",
            self.render_header_box_row()
            + self.render_box_grid()
            + [self.render_title()],
            dict(
                width=self.WIDTH,
                height=self.HEIGHT,
                font_family="Ubuntu Mono",
            ),
        )
