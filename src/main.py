import network
import json
import socket
import time
from wifi_tools import connect_to_wifi
from led_strip import LedStrip, Color

led_strip = LedStrip()
led_strip.fill(Color(242,164,28))

def load_html(path_to_html_file:str = 'assets/index.html')->str:
    html = """<!DOCTYPE html><html><head><title>failed to load html data</title></head></html>"""
    
    with open(path_to_html_file, 'r') as file:
        html_str = file.read()

    return  html_str

ip = connect_to_wifi()
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

def home_page(cl, params, named_params):
    print("home page")
    page_str = load_html("assets/index.html")
    cl.send(page_str.format(example_variable =  "Variable secured"))
    
def test2_page(cl, params, named_params):
    page_str = load_html("assets/index.html")
    print("returning test2 page")
    cl.send(page_str.format(example_variable =  "TEST2"))

def page_not_found(cl):
    cl.send(load_html("assets/404_page.html"))

routes_map = {"/": home_page, "/test2":test2_page}

def parse_uri(uri:str):
    params_separator = uri.find("?")
    if params_separator == -1:
        return uri, [], {}
    
    path = uri[:params_separator]
    params = uri[params_separator+1:].split('&')
    
    positional_params = []
    named_parameters = {}
    
    for param in params:
        if param.find('=') == -1:
            positional_params.append(param)
        else:
            named_parameters[param.split("=")[0]] = param.split("=")[1]
            
    return path.strip(), positional_params, named_parameters

def redirect(ip , cl):
    
    request = cl.recv(1024)
    begin = str(request).find("GET")
    referer_str = str(request)[begin:].split("\\n")[0]
    referer_str = referer_str[3:-10]

    route_str = referer_str.strip()
    path, positional_params, named_parameters = parse_uri(route_str)
    print(f"full request: {str(request)}")
    print("path:" , path) 
    print("params:" , positional_params)
    print("named_params:" , named_parameters)
    
    if path not in routes_map:
        print(f"page: {path} was not in routes_map")
        # page_not_found(cl)
        return
    
    try:
        routes_map[path](cl, positional_params, named_parameters)
    except Exception as err:
        print(err)
    
print(f"listening on: http://{ip}")

while True:
    try:
        cl, addr = s.accept()
        redirect(ip, cl)
        print('client connected from', addr)
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')