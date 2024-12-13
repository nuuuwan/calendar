import calendar
import os

from utils import Log, TimeFormat, _

log = Log("MonthCalendar")


class MonthCalendar:
    WIDTH = 1_600
    HEIGHT = int(WIDTH * 9 / 16)
    PADDING = 100
    DISPLAY_WIDTH = WIDTH - 2 * PADDING
    DISPLAY_HEIGHT = HEIGHT - 2 * PADDING

    N_X = 7
    N_Y = 6
    BOX_WIDTH = DISPLAY_WIDTH / N_X
    BOX_HEIGHT = DISPLAY_HEIGHT / N_Y

    @staticmethod
    def point(px, py):
        x = MonthCalendar.PADDING + px * (MonthCalendar.DISPLAY_WIDTH)
        y = MonthCalendar.PADDING + py * (MonthCalendar.DISPLAY_HEIGHT)
        return dict(x=x, y=y)

    def __init__(self, year, month):
        self.year = year
        self.month = month

    @property
    def time(self):
        return TimeFormat("%Y-%m").parse(f"{self.year}-{self.month:02d}")

    @property
    def svg_path(self):
        return os.path.join("images", f"{self.year}-{self.month:02d}.svg")

    def render_title(self):
        return _(
            "text",
            TimeFormat("%Y %B").stringify(self.time),
            self.point(0.5, -0.07) | dict(font_size=30),
        )

    def render_box_grid(self):
        box_list = []

        cal = calendar.Calendar()
        days = list(cal.itermonthdays(self.year, self.month))

        for i, day in enumerate(days):
            x = i % self.N_X
            y = i // self.N_X
            box = _(
                "g",
                [
                    _(
                        "rect",
                        None,
                        dict(
                            fill="none",
                            stroke="black",
                            width=self.BOX_WIDTH,
                            height=self.BOX_HEIGHT,
                        )
                        | self.point(x / self.N_X, y / self.N_Y),
                    ),
                    _(
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
                    ),
                ],
            )
            box_list.append(box)
        return box_list

    def render_header_box_row(self):

        header_box_row = []
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
                            font_size=20,
                            width=self.DISPLAY_WIDTH / 7,
                            height=self.DISPLAY_HEIGHT / 6,
                        )
                        | self.point(
                            (x + 0.5) / self.N_X,
                            (-0.1) / self.N_Y,
                        ),
                    ),
                ],
            )
            header_box_row.append(header_box)

        return header_box_row

    def draw(self):
        svg = _(
            "svg",
            self.render_header_box_row()
            + self.render_box_grid()
            + [self.render_title()],
            dict(
                width=self.WIDTH,
                height=self.HEIGHT,
                text_anchor="middle",
                font_family="Ubuntu Mono",
            ),
        )
        svg.store(self.svg_path)
        log.info(f"Wrote {self.svg_path}")
        os.startfile(self.svg_path)


if __name__ == "__main__":
    MonthCalendar(2024, 12).draw()
