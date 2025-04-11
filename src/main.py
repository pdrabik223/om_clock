import network
import socket
import time
from helpers import connect_to_wlan


ssid = 'FurFur_2.4G'
password = 'm0n41154'

html = f"""<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1>
        <p>{12}</p>
        <button> Test </button>
    </body>
</html>
"""

connect_to_wlan(ssid, password)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)


while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)

        cl.send(html)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')