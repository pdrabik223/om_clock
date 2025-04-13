from neopixel import Neopixel


class Color:
    r = 0
    g = 0
    b = 0

    def __init__(self, r: float, g: float, b: float):
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255

        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b})"

    def to_tuple(self):
        return (self.r, self.g, self.b)

    @staticmethod
    def red():
        return Color(255, 0, 0)

    @staticmethod
    def orange():
        return Color(255, 50, 0)

    @staticmethod
    def yellow():
        return Color(255, 100, 0)

    @staticmethod
    def green():
        return Color(0, 255, 0)

    @staticmethod
    def blue():
        return Color(0, 0, 255)

    @staticmethod
    def indigo():
        return Color(100, 0, 90)

    @staticmethod
    def pink():
        return Color(200, 0, 100)

    @staticmethod
    def violet():
        return Color(50, 0, 100)

    @staticmethod
    def white():
        return Color(200, 255, 200)

    @staticmethod
    def black():
        return Color(0, 0, 0)

# No pixels used 
# 4 * 7 * 2 + 2 = 58
# displays, segments, leds per segment and divider between hour and minutes 

class LedStrip:
      
    _led_strip = Neopixel(38, 0, 3, "GRB")
    
    def __init__(self) -> None:
        self._led_strip.brightness(100)
        self._led_strip.fill(Color.red().to_tuple())
        self._led_strip.show()

    def fill(self, color: Color, show: bool = True):
        self._led_strip.fill(color.to_tuple())
        if show:
            self._led_strip.show()

    def set_pixels(
        self, indexes, color: Color, brightness: int = 100, show: bool = True
    ):
        for index in indexes:
            self._led_strip.set_pixel(index, color.to_tuple(), how_bright=brightness)
        if show:
            self._led_strip.show()

    def set_pixel(
        self, index: int, color: Color, brightness: int = 100, show: bool = True
    ):
        self._led_strip.set_pixel(index, color.to_tuple(), how_bright=brightness)
        if show:
            self._led_strip.show()

    def show(self):
        self._led_strip.show()

    def brightness(self, brightness: int, show: bool = True):
        self._led_strip.brightness(brightness)
        if show:
            self._led_strip.show()

