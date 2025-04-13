import network
import json
import socket
import time
from wifi_tools import connect_to_wifi
from led_strip import LedStrip

led_strip = LedStrip()

def load_html(path_to_html_file:str = 'assets/index.html'):
    html = """<!DOCTYPE html><html><head><title>failed to load html data</title></head></html>"""
    
    with open(path_to_html_file, 'r') as file:
        html_str =  file.read()

    return  html_str

html = load_html()

ip = connect_to_wifi()
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)


# @endpoint("")
def home_page(cl):
    print("home page")
    cl.send(html)
    
    

routes_map = {"": home_page}

def endpoint(path:str):
    def endpoint_decorator(func):
        def wrapper(*args, **kwargs):
            print("wrapper")
            routes_map[path] = lambda : func(*args, **kwargs)
            return
        return wrapper
    return endpoint_decorator
    
def redirect(ip , cl):
    
    request = cl.recv(1024)
    begin = str(request).find("Referer:")
    referer_str = str(request)[begin:].split("\\n")[0]
    route_str = referer_str[8:-2]

    route_str = route_str[len("http://") + len(ip) + 1:].strip()
    print(route_str)
    try:
        routes_map[route_str](cl)
    except Exception as err:
        print(err)
    
print(f"listening on: http://{ip}\nlist of endpoints: {routes_map}")

while True:
    try:
        cl, addr = s.accept()
        redirect(ip, cl)
        print('client connected from', addr)
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')