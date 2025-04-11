import network
import socket
import time
from helpers import connect_to_wlan


ssid = 'FurFur_2.4G'
password = 'm0n41154'

connect_to_wlan(ssid, password)

def load_html():
    html = """<!DOCTYPE html><html><head><title>ERROR</title></head></html>"""
    
    with open('assets/index.html', 'r') as file:
        html =  file.read().format(example_variable = 22)

    return  html

html = load_html()

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        begin = str(request).find("Referer:")
        referer_str = str(request)[begin:].split("\\n")[0]
        route_str =  referer_str[8:-2]
        # end = request.find("Accept-Encoding")
        print(route_str.strip())
        
        
        cl.send(html)
        cl.close()
        time.sleep(0.1)
    except OSError as e:
        cl.close()
        print('connection closed')