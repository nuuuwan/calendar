import os
from abc import ABC

from utils import Log

log = Log("AbstractCalendar")


class AbstractCalendar(ABC):
    ASPECT_RATIO = (0.5 + 8.3) / 11.7
    WIDTH = 1_200
    HEIGHT = int(WIDTH * ASPECT_RATIO)
    PADDING = 100
    DISPLAY_WIDTH = WIDTH - 2 * PADDING
    DISPLAY_HEIGHT = HEIGHT - 2 * PADDING

    @staticmethod
    def point(px, py):
        x = int(
            AbstractCalendar.PADDING + px * (AbstractCalendar.DISPLAY_WIDTH)
        )
        y = int(
            AbstractCalendar.PADDING + py * (AbstractCalendar.DISPLAY_HEIGHT)
        )
        return dict(x=x, y=y)

    @property
    def time(self):
        return self.time_format.parse(str(self))

    @property
    def svg_path(self):
        return os.path.join("images", f"{str(self)}.svg")

    def draw(self):
        svg = self.render()
        svg.store(self.svg_path)
        log.info(f"Wrote {self.svg_path}")
       