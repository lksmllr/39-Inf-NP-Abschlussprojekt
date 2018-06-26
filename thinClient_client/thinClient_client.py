#!/usr/bin/env python3

import requests, json, uuid
import os, sys, platform, subprocess
import argparse, shlex
import time
from sh import cd
from threading import Thread

thinClient_server_URL = '127.0.0.1:5000'
thinClient_server_heartbeat_URL = 'http://'+thinClient_server_URL+'/heartbeat/'
thinClient_server_list_packages_URL = 'http://'+thinClient_server_URL+'/list_packages/'
thinClient_server_resource_URL = 'http://'+thinClient_server_URL+'/resources/'
wrong_args = 'Type -h for help!'
quit_ui = False

# update package with id package_id
def update(package_id):
    pass

# install package with id package_id
def upgrade(package_id):
    r = requests.post(thinClient_server_resource_URL, data={'package_id': package_id})
    f = open(package_id, 'w')
    f.write(str(r.content))
    f.close()


# list available packages
def list_packages():
    print('\nAvailable Packages are:\n')
    r = requests.get(thinClient_server_list_packages_URL)
    packages = json.loads(r.text)
    for p in packages:
        print(p)
    print()

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
    con_refused = False
    printed = False
    while(quit_ui is not True):
        try:
            r = requests.post(thinClient_server_heartbeat_URL
                , data={'id': my_id, 'cpu': my_cpu, 'ram': my_ram, 'gpu': my_gpu})
            #if r.status_code is 200:
                #print('Client: '+get_mac_adress()+' sent heartbeat to: '+thinClient_server_heartbeat_URL)
            #print(r.status_code, r.reason)
            printed = False
        except Exception as e:
            if printed is not True:
                print('\n'+e)
                print("\nConnection refused!\n")
                printed = True
        time.sleep(1)

# main loop for user interactions and or commands (shell-like)
# offers use of system commands like ls, cd
def user_interface():
    global quit_ui, wrong_args, t

    t.start()

    print("\033[H\033[J")
    print('Welcome to your ThinClient- Shell!')
    print('\nType -h or --help for usage information.\n')

    while(quit_ui is not True):
        sys_path = os.getcwd()
        sys_path = sys_path.split('/')
        my_path = '/'+sys_path[len(sys_path)-1]

        user_input = input(my_path+" ThinClientShell>>")
        try:
            parser = argparse.ArgumentParser(description="ThinClientShell")
            parser.add_argument("-q", "--quit", action="store_true"
            , default=False, help="Quit ThinClientShell")
            parser.add_argument("-cd", help="Change working directory")

            # package functions
            parser.add_argument("-p", "--packages", action="store_true"
            , help="List available packages")
            parser.add_argument("-u", "--update"
            , help="Update Package with package_id")
            parser.add_argument("-i", "--install"
            , help='Install package with id package_id')

            # client functions
            parser.add_argument("-lc", "--listclients"
            , help="List all server known clients")
            parser.add_argument("-a", "--alive"
            , help="Online status of client with id client_id")
            parser.add_argument("-inf", "--info"
            , help="Information about client with id client_id")

            args, unknown = parser.parse_known_args(shlex.split(user_input))

            if args.quit:
                print('\nGood bye &nd have a great day!\n')
                quit_ui = True
            elif args.packages:
                list_packages()
            elif args.update:
                update(args.update)
                print('updating ...')
            elif args.install:
                upgrade(args.install)
            elif args.cd:
                cd(args.cd)
                """
                maybe auto completion, see
                https://edwards.sdsu.edu/research/autocompletion-in-default-python-shell/
                """
            else:
                try:
                    subprocess.run(user_input, shell=True, check=False)
                except SystemExit as e:
                    # dont raise error
                    pass
        except SystemExit as e:
            # dont raise error
            pass

t = Thread(target=send_heartbeat)
user_interface()
