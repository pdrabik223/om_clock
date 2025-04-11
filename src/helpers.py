import network
import time


def connect_to_wlan(ssid:str, password:str, retry_attempts:int = 10):
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
        
    while retry_attempts > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        retry_attempts -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0])
