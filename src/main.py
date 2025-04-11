from led_strip import LedStrip, Color
from machine import Pin
import time
led_strip = LedStrip()

     

Pin('LED', Pin.OUT).value(1)

i=0
while(True):
    i += 1
    led_strip.fill(Color.black())
    led_strip.set_pixel(i%38,Color.red())
    time.sleep(0.1)
    
