"""!@brief Main script for scraping from Socialblade.

To get as much data as possible from the website, we look for the top 250 channels in more than 240 available
country options for a total of > 60.000 channels. These channels are the most successful ones in their respective
country, so we assume the data to be representative of the countries Youtube activities.

First, the scraper gets all available country top channel urls and assembles work packages from the results. Then docker
containers are used to connect to a VPN, each with a different IP to avoid blocking by Cloudflare. Each container gets
a work package assigned. Once all containers finished scraping for the urls of the top 250 channels per country, new
work packages are created and again assigned to docker containers with random IPs. After completion of all tasks, the
data gets assembled into a single data file.

@file Scrape main script file.
@author Niklas Landerer
@author Martin Schuck
@date 18.6.2020
"""

import json
import os
import time
import requests
import random
from sb_scraper import SBScraper


PATH = "/"
package_id = os.environ['PACKAGE']
load_save = True if os.environ['LOAD_FILE'] == "yes" else False

def load_channel_urls(package_id):
    work_package_path = os.path.join(PATH, 'work_packages', 'package_' + str(package_id))
    with open(os.path.join(work_package_path, 'job.json'), 'r') as f:
        channel_url_list = json.load(f)
    return channel_url_list


def load_quicksave(package_id):
    work_package_path = os.path.join(PATH, 'work_packages', 'package_' + str(package_id))
    with open(os.path.join(work_package_path, 'quicksave.json'), 'r') as f:
        quicksave = json.load(f)
    return quicksave


def clear_dictionary(package_id):
    work_package_path = os.path.join(PATH, 'work_packages', 'package_' + str(package_id))
    for filename in ['results.json', 'quicksave.json']:
        if os.path.isfile(os.path.join(work_package_path, filename)):
            os.remove(os.path.join(work_package_path, filename))


def show_dialogue(dialogue_nr=0):
    if dialogue_nr == 0:
        print('#####################################################')
        print('###  Warning: Script is supposed to run on Linux! ###')
        print('###     NordVPN has to be installed in advance    ###')
        print('#####################################################')
        print('#####################################################')
        print('###         Starting Socialblade scraper.         ###')
        print('### Please enter the package you want to work on! ###')
        print('#####################################################')
        package_id = int(input())
        while not os.path.isfile(os.path.join(PATH, 'work_packages', 'package_' + str(package_id), 'job.json')):
            print('#####################################################')
            print('###         Please enter a valid package!         ###')
            print('#####################################################')
            package_id = int(input())
        else:
            print('#####################################################')
            print('###          Working on package number {:2d}         ###'.format(package_id))
            print('#####################################################')
        print('\n#####################################################')
        print('###   Do you want to load a quicksave? (yes/no)   ###')
        print('#####################################################')
        return package_id, input().lower() == 'yes'
    if dialogue_nr == 1:
        print('##################################')
        print('###  Finished working package  ###')
        print('### The scraper will now close ###')
        print('##################################')


def write_results(results, package_id):
    with open(os.path.join(PATH, 'work_packages', 'package_' + str(package_id), 'results.json'), 'w') as f:
        json.dump(results, f)


def quicksave(channel_url_list, results):
    save = {'channel_url_list': channel_url_list,
            'results': results}
    with open(os.path.join(PATH, 'work_packages', 'package_' + str(package_id), 'quicksave.json'), 'w') as f:
        json.dump(save, f)


def change_vpn(server):
    os.system('nordvpn disconnect')
    server = server.split('.')[0]
    os.system('nordvpn connect ' + server)


def get_vpn_servers():
    req = requests.get("https://api.nordvpn.com/v1/servers?limit=10000")
    vpn_list = []
    for server in req.json():
        if server["load"] < 50:
            vpn_list.append(server["hostname"])
    random.shuffle(vpn_list)
    print('VPN Server list has length: {}'.format(len(vpn_list)))
    return vpn_list


if __name__ == '__main__':
    # package_id, load_save = show_dialogue(dialogue_nr=0)
    if load_save:
        save = load_quicksave(package_id)
        channel_url_list = save['channel_url_list']
        results = save['results']
    else:
        channel_url_list = load_channel_urls(package_id)
        results = list()
    clear_dictionary(package_id)

    sb_scraper = SBScraper()

    # Connect to VPNs to avoid getting blocked by cloudflare.
    vpn_server_list = get_vpn_servers()
    while not vpn_server_list:
        vpn_server_list = get_vpn_servers()
    change_vpn(vpn_server_list.pop())

    tot_len = len(channel_url_list)
    it = 1
    err_cnt = 0
    while channel_url_list:
        channel_url = channel_url_list.pop()
        channel_data = sb_scraper.get_channel_data(channel_url)
        if not channel_data:
            print('### WARNING: SCRAPING CHANNEL FAILED ###')
            err_cnt += 1
            if err_cnt < 25:  # In case a bad link was passed, give up parsing after 20 tries.
                channel_url_list.append(channel_url)
            else:
                err_cnt = 0
            while not vpn_server_list:
                vpn_server_list = get_vpn_servers()
            change_vpn(vpn_server_list.pop())
        else:
            err_cnt = 0
            print('Scraping at {:.2f}%'.format((1 - len(channel_url_list)/tot_len)*100))
            results.append(channel_data)
        if not it % 50:
            print('Quicksaving...')
            quicksave(channel_url_list, results)
        it += 1
        # time.sleep(random.uniform(2., 3.))
    if results:
        write_results(results, package_id=package_id)
    show_dialogue(dialogue_nr=1)
    time.sleep(1)

