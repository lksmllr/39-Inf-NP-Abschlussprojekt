#!/usr/bin/env python3

import requests, json, uuid
import os, sys, platform
import argparse, shlex

thinClient_server_heartbeat_URL = 'http://127.0.0.1:5000/heartbeat/'
wrong_args = 'Type -h for help!'
quit_ui = False

# shell like loop for user interactions and or commands
def user_interface():
    global quit_ui, wrong_args

    print("\033[H\033[J")
    print('Welcome to your ThinClient- Shell!')
    print('\nType -h or --help for usage information.\n')

    while(quit_ui is not True):
        user_input = input("ThinClientShell>>")
        try:
            parser = argparse.ArgumentParser(description="ThinClientShell")
            parser.add_argument("-q", "--quit", action="store_true", default=False, help="Quit ThinClientShell")
            parser.add_argument("-p", "--packages", action="store_true", help="List available packages")
            parser.add_argument("-u", "--update", help="Update Package with package_id")
            args = parser.parse_args(shlex.split(user_input))

            if args.quit:
                quit_ui = True
            elif args.packages:
                list_packages()
                print('Package- list')
            elif args.update:
                update(args.update)
                print('updating ...')

        except SystemExit:
            pass

# update package with id package_id
def update(package_id):
    pass

# install package with id package_id
def upgrade(package_id):
    pass

# list available packages
def list_packages():
    pass

# show information about other client
def show(client_id):
    pass

# ask server if specific client is online now
def alive(client_id):
    pass

# list all ThinClients
def list_clients():
    pass

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

#send_heartbeat()
user_interface()
