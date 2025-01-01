import abc


@abc
class AbstractCalendar:
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
