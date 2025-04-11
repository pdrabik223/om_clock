import network
import socket
import time
from helpers import connect_to_wlan


ssid = 'FurFur_2.4G'
password = 'm0n41154'

ip = connect_to_wlan(ssid, password)

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


def test2_endpoint():
    print("running endpoint code")
    
routes_map = {"test2": test2_endpoint()}

def redirect(route_str:str):
    route_str = route_str[len("http://") + len(ip) + 1:]
    print(route_str)
    # if routes_map.keys().contains(route_str)
        # routes_map[route_str]()
    
    
    
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        begin = str(request).find("Referer:")
        referer_str = str(request)[begin:].split("\\n")[0]
        route_str =  referer_str[8:-2]
        redirect(route_str)
        
        cl.send(html)
        cl.close()
        time.sleep(0.1)
    except OSError as e:
        cl.close()
        print('connection closed')