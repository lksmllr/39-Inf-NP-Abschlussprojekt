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

# change if u like another dir to install packages
install_dir = os.getcwd()

wrong_args = 'Type -h for help!'
quit_ui = False

# split file name to get the name of the package without version and ending
def get_package_name(file):
    f_tmp = file.split('.')[0]
    f_prefix = f_tmp.split('_')
    return f_prefix[0]

# split the file name to get only the version
def get_version(file):
    f_tmp = file.split('.')[0]
    f_prefix = f_tmp.split('_')
    return f_prefix[len(f_prefix)-1]

# update package with id package_id
# this will replace old package with the new version
def update(package_id):
    error = None
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
                        # remove old folder
                        subprocess.run('rm -r '+f_installed_name, shell=True, check=False)
                        # install update
                        subprocess.run('unzip '+package_id+' -d'+package_name, shell=True, check=False)
                    except SystemExit as e:
                        error = e
                        print('\n'+str(e)+'\n')
            else:
                print('\nPackage \"'+package_name+'\" already up-to-date.\n')
        else:
            # install it ?
            pass


# install package with id package_id
# get file from server and install it in a folder
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
                subprocess.run('unzip '+package_id+' -d'+get_package_name(package_id), shell=True, check=False)
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


# list available packages on the thinClien_server
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
