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
import math
import time
import glob
import random
import shutil
from sb_scraper import SBScraper


PATH = os.path.join(os.path.abspath(""))


def assemble_work_packages(url_list, n_packages):
    shutil.rmtree(os.path.join(PATH, 'work_packages'))
    package_size = math.ceil(len(url_list) / n_packages)
    work_packages = [url_list[x:x + package_size] for x in range(0, len(url_list), package_size)]
    for idx, package in enumerate(work_packages):
        os.makedirs(os.path.join(PATH, 'work_packages', 'package_' + str(idx)))
        with open(os.path.join(PATH, 'work_packages', 'package_' + str(idx), 'job.json'), 'w') as f:
            json.dump(package, f)
    with open(os.path.join(PATH, 'work_packages', 'results.json'), 'w') as f:  # Save the deleted results file again.
        json.dump(url_list, f)


def load_country_results(result_file='results.json'):
    channel_url_list = list()
    with open(os.path.join(PATH, 'work_packages', result_file), 'r') as f:
        country_list = json.load(f)
        for country_dict in country_list:
            for key in country_dict.keys():
                channel_url_list.extend(country_dict[key])
    return channel_url_list


def clear_dictionaries():
    work_packages_path = os.path.join(PATH, "work_packages")
    for directory in [d for d in os.listdir(work_packages_path) if os.path.isdir(os.path.join(work_packages_path, d))]:
        r_files = glob.glob(os.path.join(work_packages_path, directory) + '/*')
        for f in r_files:
            print(f)
            os.remove(f)
        os.rmdir(os.path.join(work_packages_path, directory))
    r_files = glob.glob(os.path.join(work_packages_path, '*'))
    for f in r_files:
        os.remove(f)


def show_dialogue(dialogue_nr=0):
    if dialogue_nr == 0:
        print('##########################################################')
        print('###   You are about to assemble new working packages   ###')
        print('### ALL DATA IN THE WORK PACKAGES FOLDERS WILL BE LOST ###')
        print('###               Please confirm! (yes/no)             ###')
        print('##########################################################')
        rsp = (input().lower() == 'yes')
        if rsp:
            print('\n##########################################################')
            print('###                    Confirmed                       ###')
            print('##########################################################')
        else:
            print('\n##########################################################')
            print('###                     Aborted                        ###')
            print('##########################################################')
        return rsp
    if dialogue_nr == 1:
        print('########################################')
        print('###      Finished country scrape     ###')
        print('###  Create new packages (yes/no)?   ###')
        print('########################################')
        rsp = (input().lower() == 'yes')
        if rsp:
            print('\n##########################################################')
            print('###                    Confirmed                       ###')
            print('##########################################################')
        else:
            print('\n##########################################################')
            print('###                     Aborted                        ###')
            print('##########################################################')
        return rsp
    if dialogue_nr == 2:
        print('##################################################################')
        print('### Enter the number of working packages do you want to create ###')
        print('##################################################################')
        rsp = int(input())
        return rsp


def write_fails(fails):
    with open(os.path.join(PATH, 'work_packages', 'fails.json'), 'w') as f:
        json.dump(fails, f)


def write_results(results):
    with open(os.path.join(PATH, 'work_packages', 'results.json'), 'w') as f:
        json.dump(results, f)


if __name__ == '__main__':
    confirm = show_dialogue(dialogue_nr=0)
    if confirm:
        clear_dictionaries()

        failed_urls = list()
        results = list()

        sb_scraper = SBScraper()
        country_url_list = sb_scraper.get_all_country_urls()
        tot_len = len(country_url_list)
        while country_url_list:
            country_url = country_url_list.pop()
            country_channels = sb_scraper.get_channels_by_country(country_url)
            if not country_channels:
                print('### WARNING: SCRAPING COUNTRY FAILED ###')
                failed_urls.append(country_url)
            else:
                print('Scraping at {:.2f}%'.format((1 - len(country_url_list)/tot_len)*100))
                results.append(country_channels)
            time.sleep(random.uniform(2., 3.))
        if failed_urls:
            write_fails(failed_urls)
        if results:
            write_results(results)
    confirm = show_dialogue(dialogue_nr=1)
    if confirm:
        channel_urls = load_country_results()
        n_packages = show_dialogue(dialogue_nr=2)
        assemble_work_packages(channel_urls, n_packages=n_packages)
        print('Working packages assembled.')
