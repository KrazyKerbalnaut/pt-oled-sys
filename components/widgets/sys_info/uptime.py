# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

from datetime import datetime
import psutil
import math
from components.widgets.common.functions import title_text, right_text, draw_text
from components.widgets.common.values import (
    default_margin_x,
    default_margin_y,
    common_first_line_y,
    common_second_line_y,
    common_third_line_y
)
from components.widgets.common.base_widgets import BaseSnapshot

class Hotspot(BaseSnapshot):
    def __init__(self, width, height, mode, interval, **data):
        super(Hotspot, self).__init__(width, height, interval, Hotspot.render)

    @staticmethod
    def render(draw, width, height):
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        elapsed = datetime.now() - boot_time
        time = int(elapsed.total_seconds())

        time_s = "{0}".format(time)
        timeS = time % 60
        timeM = math.floor(time / 60) % 60
        timeH = math.floor(time / 3600) % 24
        timeD = math.floor(time / 86400)
        timeDHMS = "{0} days, {1}:{2:02d}:{3:02d}".format(int(timeD), int(timeH), int(timeM), int(timeS))


        title_text(draw, default_margin_y, width=width, text="Uptime")

        draw_text(draw, xy=(default_margin_x, common_first_line_y), text="Since boot:")
        title_text(draw, y=common_second_line_y, width=width+12, text=timeDHMS)

        draw_text(draw, xy=(default_margin_x, common_third_line_y), text="Seconds:")
        right_text(draw, y=common_third_line_y, width=width, text=time_s)