import network
import json
import socket
import time
from wifi_tools import connect_to_wifi
from led_strip import LedStrip, Color

led_strip = LedStrip()
led_brightness = 100
led_color = Color(242, 164, 28)
led_strip.brightness(led_brightness, False)
led_strip.fill(led_color)


def load_html(path_to_html_file: str = "assets/index.html") -> str:
    error_html = """<!DOCTYPE html><html><head><title>failed to load html data</title></head></html>"""

    with open(path_to_html_file, "r") as file:
        html_str = file.read()
    # TODO on error return error html info
    return html_str

ip = connect_to_wifi()


def home_page(cl, params, named_params):
    global led_color
    global led_brightness
    global led_strip

    brightness = named_params.get("brightness", None)
    if brightness != None:
        led_brightness = int(brightness)
        led_strip.brightness(led_brightness)

    color_str = named_params.get("color", None)
    if color_str != None:
        color_str = color_str[-6:]
        led_color = Color(*tuple(int(color_str[i : i + 2], 16) for i in (0, 2, 4)))
        led_strip.fill(led_color)

    page_str = load_html("assets/index.html")
    hex_color = "#%02x%02x%02x" % led_color.to_tuple()
    cl.send(page_str.format(brightness=led_brightness, color=hex_color))


def page_not_found(cl):
    cl.send(load_html("assets/404_page.html"))


class WifiConnectionHandler:
    def __init__(
        self,
        ssid: str = None,
        password: str = None,
        config_file_path="wifi_config.json",
    ):
        pass

    # TODO monitor wifi connection and retry when it's broken
    def check_wifi_connection():
        # check if wifi is connected and in range, retry connection if not, returns true or raises error
        pass


class App:
    def __init__(self):
        addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
        self.socket = socket.socket()
        self.socket.bind(addr)
        self.socket.listen(1)
        self.routes_map = {}

        pass

    def __parse_uri(self, uri: str):
        params_separator = uri.find("?")
        if params_separator == -1:
            return uri, [], {}

        path = uri[:params_separator]
        params = uri[params_separator + 1 :].split("&")

        positional_params = []
        named_parameters = {}

        for param in params:
            if param.find("=") == -1:
                positional_params.append(param)
            else:
                named_parameters[param.split("=")[0]] = param.split("=")[1]

        return path.strip(), positional_params, named_parameters

    def __redirect(self, ip, cl):

        request = cl.recv(1024)
        begin = str(request).find("GET")
        referer_str = str(request)[begin:].split("\\n")[0]
        referer_str = referer_str[3:-10]

        route_str = referer_str.strip()
        path, positional_params, named_parameters = self.__parse_uri(route_str)

        if path not in routes_map:
            print(f"page: {path} was not in routes_map")
            return

        # try:
        routes_map[path](cl, positional_params, named_parameters)
        # except Exception as err:
        #     print(err)

    def main_loop(self):
        print(f"listening on: http://{ip}")

        while True:
            try:
                cl, _ = self.socket.accept()
                self.__redirect(ip, cl)

                cl.close()
            except OSError as e:
                cl.close()
                print("connection closed")

    def endpoint(self, path: str, func: function):
        pass

    def page_not_found_endpoint(self, func: function):
        pass


app = App()
app.main_loop()
