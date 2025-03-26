from led_strip import LedStrip, Color
from machine import Pin

LED_STRIP = LedStrip()
#LED_STRIP.fill(Color.black())
#LED_STRIP.fill(Color.red())
Pin('LED', Pin.OUT).value(1)
   