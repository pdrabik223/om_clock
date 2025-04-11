import network
import json
import time

def connect_to_wlan(ssid:str, password:str, retry_attempts:int = 10)-> str:
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
        
    while retry_attempts > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        retry_attempts -= 1
        print('connecting...')
        time.sleep(1)

    if wlan.status() != 3:
        print('connection failed')
        raise RuntimeError('network connection failed')

    else:
        print('connection succeeded')

        status = wlan.ifconfig()
        return status[0]    

def get_wifi_info()->dict:
    wifi_config = {}
    try:
        with open("wifi_config.json", 'r') as file:
            wifi_config = json.loads(file.read())
    except Exception as err:
        print("wifi_config.json file not found")
        raise Exception("wifi_config.json file not found")
    
    return wifi_config


def connect_to_wifi()->str:
    wifi_list = get_wifi_info()
    print(f"loaded wifi list: {wifi_list}")
    
    for i in wifi_list.keys():
        print(f"connecting to wifi: {i} with password: {wifi_list[i]}")
        try:
            return connect_to_wlan(i, wifi_list[i])
        except Exception as err:
            continue

    raise RuntimeError("network connection failed")
