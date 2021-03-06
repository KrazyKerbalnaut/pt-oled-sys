from pitopcommon.sys_info import (
    get_wifi_network_ssid,
    get_internal_ip,
    get_network_strength,
)
from components.widgets.common.functions import draw_text, get_image_file_path, right_text
from components.widgets.common.values import (
    default_margin_x,
    common_second_line_y,
    common_third_line_y,
)
from components.widgets.common.base_widgets import BaseSnapshot
from components.widgets.common.image_component import ImageComponent
from ipaddress import ip_address


def wifi_strength_image():
    wifi_strength = int(get_network_strength("wlan0")[:-1]) / 100
    wifi_rating = "sys_info/wifi_strength_bars/"
    if wifi_strength <= 0:
        wifi_rating += "wifi_no_signal.gif"
    elif 0 < wifi_strength <= 0.5:
        wifi_rating += "wifi_weak_signal.gif"
    elif 0.4 < wifi_strength <= 0.6:
        wifi_rating += "wifi_okay_signal.gif"
    elif 0.6 < wifi_strength <= 0.7:
        wifi_rating += "wifi_good_signal.gif"
    else:
        wifi_rating += "wifi_excellent_signal.gif"

    return get_image_file_path(f"{wifi_rating}")


class Hotspot(BaseSnapshot):
    def __init__(self, width, height, mode, interval, **data):
        super(Hotspot, self).__init__(width, height, interval, self.render)
        self.width = width
        self.height = height
        self.mode = mode
        self.gif = ImageComponent(
            device_mode=self.mode,
            width=self.width,
            height=self.height,
            image_path=get_image_file_path("sys_info/wifi.gif"),
            loop=False,
            playback_speed=2.0,
        )

        self.wifi_id = ""
        self.wlan0_ip = ""
        self.wifi_bars_image = ""
        self.initialised = False

        self.default_interval = interval

    def reset(self):
        self.gif = ImageComponent(
            device_mode=self.mode,
            width=self.width,
            height=self.height,
            image_path=get_image_file_path("sys_info/wifi.gif"),
            loop=False,
            playback_speed=2.0,
        )

        self.wifi_id = ""
        self.wlan0_ip = ""
        self.wifi_bars_image = ""
        self.initialised = False

        self.interval = self.default_interval

    def is_connected(self):
        return self.wlan0_ip != ""

    def set_data_members(self):
        network_ssid = get_wifi_network_ssid()
        if network_ssid != "Error":
            self.wifi_id = network_ssid

        network_ip = get_internal_ip(iface="wlan0")
        try:
            self.wlan0_ip = ip_address(network_ip)
        except ValueError:
            self.wlan0_ip = ""

        self.wifi_bars_image = wifi_strength_image()

        if not self.is_connected():
            self.gif = ImageComponent(
                device_mode=self.mode,
                width=self.width,
                height=self.height,
                image_path=get_image_file_path("sys_info/wifi.gif"),
                loop=False,
                playback_speed=2.0,
            )

        self.gif.hold_first_frame = not self.is_connected()
        self.initialised = True

    def render(self, draw, width, height):
        first_frame = not self.initialised

        # Determine initial connection state
        if first_frame:
            self.set_data_members()

        # Determine connection state
        if not self.gif.is_animating():
            self.set_data_members()

        # Determine animation speed
        # TODO: fix frame speed in GIF
        # self.interval = self.gif.frame_duration
        if first_frame:
            self.interval = 0.5
        else:
            if self.gif.is_animating():
                self.interval = 0.025
            else:
                self.interval = self.default_interval

        # Draw to OLED
        self.gif.render(draw)

        if self.initialised and not self.gif.is_animating():
            if self.is_connected() and self.gif.finished:
                wifi_bars = ImageComponent(
                    device_mode=self.mode,
                    width=self.width,
                    height=self.height,
                    xy=(5, 0),
                    image_path=self.wifi_bars_image,
                    loop=True,
                )
                wifi_bars.render(draw)

                draw_text(
                    draw,
                    xy=(default_margin_x+22, common_second_line_y-6),
                    text=str(self.wifi_id)
                )

                draw_text(
                    draw,
                    xy=(default_margin_x+22, common_third_line_y-5),
                    text=str(self.wlan0_ip)
                )
            elif not self.is_connected() and self.gif.hold_first_frame:
                draw.ellipse((69, 21) + (83, 35), 0, 0)
                draw.ellipse((70, 22) + (82, 34), 1, 0)
                draw.line((73, 25) + (78, 30), "black", 2)
                draw.line((74, 30) + (79, 25), "black", 2)