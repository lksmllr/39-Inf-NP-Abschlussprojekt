#!/usr/bin/env python3

import requests, json, uuid
import os, sys, platform

thinClient_server_heartbeat_URL = 'http://127.0.0.1:5000/heartbeat/'

# returns mac adress of this machine
def get_mac_adress():
    num = hex(uuid.getnode()).replace('0x','').replace('L','')
    mac = ':'.join(num[i:i+2] for i in range(0,11,2))
    mac = mac.zfill(12)
    return mac

# returns cpu model name of this machine
def get_cpu():
    return platform.processor()

# returns memory size of this machine
def get_ram():
    bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    gb = int(bytes / (1024.**3))
    return gb

# returns gpu model name of this machine
def get_gpu():
    return "-"

# Sends a signal to the server with hardware information
def send_heartbeat():
    my_id = get_mac_adress()
    my_cpu = get_cpu()
    my_ram = get_ram()
    my_gpu = get_gpu()
    print(get_ram())
    r = requests.post(thinClient_server_heartbeat_URL
        , data={'id': my_id, 'cpu': my_cpu, 'ram': my_ram, 'gpu': my_gpu})
    if r.status_code is 200:
        print('Client: '+get_mac_adress()
        +' sent heartbeat to: '+thinClient_server_heartbeat_URL)
    print(r.status_code, r.reason)

send_heartbeat()
