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
thinClient_server_listclients_URL = 'http://'+thinClient_server_URL+'/listclients/'
thinClient_server_showclient_URL = 'http://'+thinClient_server_URL+'/showclient/'

# change if u like another dir to install packages
install_dir = os.getcwd()

wrong_args = 'Type -h for help!'
quit_ui = False

def get_package_name(file):
    f_tmp = file.split('.')[0]
    f_prefix = f_tmp.split('_')
    return f_prefix[0]

def get_version(file):
    f_tmp = file.split('.')[0]
    f_prefix = f_tmp.split('_')
    return f_prefix[len(f_prefix)-1]

# update package with id package_id
def update(package_id):
    package_name = get_package_name(package_id)
    package_version = get_version(package_id)

    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.zip')]
    for f in files:
        f_installed_name = get_package_name(f)
        f_installed_version = get_version(f)
        if str(package_name) == str(f_installed_name):
            if int(f_installed_version) < int(package_version):
                try:
                    # download update
                    try:
                        # remove old
                        # install update
                        pass
                    except SystemExit as e:
                        pass

                except requests.exceptions.RequestException as e:
                    # error
                    pass

    error = None
    try:
        pass
    except requests.exceptions.RequestException as e:
        error = e
        print('\n'+str(e)+'\n')
        pass
    if error is None:
        pass

# install package with id package_id
def upgrade(package_id):
    error = None
    try:
        r = requests.post(thinClient_server_resource_URL
        , data={'package_id': package_id})
    except requests.exceptions.RequestException as e:
        error = e
        print('\n'+str(e)+'\n')
    if error is None and r.status_code is requests.status_codes.codes.ALL_OK   :
        content = r.content
        if content is not None:
            f = open(package_id, 'wb')
            f.write(content)
            f.close()
            try:
                subprocess.run('unzip '+package_id, shell=True, check=False)
            except SystemExit as e:
                error = e
                print('\n'+str(e)+'\n')
            if error is None:
                print('\nInstalled '+package_id+'\n')
            else:
                print('\nSomething went wrong :(\n')
    else:
        print('\nServer: I dont have package '+package_id
        +'. Ask your local admin to add it.\n')


# list available packages
def list_packages():
    error = None
    try:
        r = requests.get(thinClient_server_list_packages_URL)
        packages = json.loads(r.text)
    except requests.exceptions.RequestException as e:
        error = e
        print('\n'+str(e)+'\n')
    if error is None:
        print('\nAvailable Packages are:\n')
        for p in packages:
            print(p)
        print()

# show information about other client
def show(client_id):
    try:
        r = requests.post(thinClient_server_showclient_URL
        , data={'client_id': client_id})
        client_info = json.loads(r.text)
        if len(client_info) > 0:
            print('\nTHIN-CLIENT-INFO\n')
            print('        ID / MAC: '+client_info[0])
            print('             CPU: '+client_info[2])
            print('             RAM: '+str(client_info[3]))
            print('             GPU: '+client_info[4])
            print('LATEST_HEARTBEAT: '+client_info[1])
            print('   IS_ALIVE(1/0): '+str(client_info[5]))
            print()
        else:
            print('\nServer doesnt know this client ...\n')
    except requests.exceptions.RequestException as e:
        print('\n'+str(e)+'\n')

# ask server if specific client is online now
def alive(client_id):
    print('\nWonder if '+str(client_id)
    +' is alive? Type -inf '+client_id+' for more information. \n')

# list all ThinClients
def list_clients():
    error = None
    try:
        r = requests.get(thinClient_server_listclients_URL)
    except requests.exceptions.RequestException as e:
        error = e
        print('\n'+str(e)+'\n')
    if error is None:
        print('\nRegistered Clients:\n')
        clients = json.loads(r.text)
        if len(clients) > 0:
            for client in clients:
                print('ID: '+str(client))
            print()
        else:
            print('Server doesnt know any ...\n')

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
                print('\n'+str(e))
                print("\nConnection refused! Type Enter...\n")
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
            parser.add_argument("-lc", "--listclients", action="store_true"
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
            elif args.install:
                upgrade(args.install)
            elif args.listclients:
                list_clients()
            elif args.info:
                show(args.info)
            elif args.alive:
                alive(args.alive)
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
