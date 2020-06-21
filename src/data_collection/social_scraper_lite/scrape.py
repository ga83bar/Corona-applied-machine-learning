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
import logging
from sb_scraper import SBScraper
from container_manager import ContainerManager


PATH = os.path.join(os.path.abspath(""))


def assemble_work_packages(url_list, n_packages):
    package_size = math.ceil(len(url_list)/n_packages)
    work_packages = [url_list[x:x + package_size] for x in range(0, len(url_list), package_size)]
    for idx, package in enumerate(work_packages):
        os.makedirs(os.path.join(PATH))


def load_country_results(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    channel_url_list = list()
    for file in files:
        with open(os.path.join(path, file), 'r') as f:
            country_dict = json.load(f)
            for key in country_dict.keys():
                channel_url_list.extend(country_dict[key])
    return channel_url_list


def clear_dictionaries():
    cl_path = os.path.join(PATH, "work_packages")
    job_files = glob.glob(cl_path + '/*')
    
    for f in job_files:
        os.remove(f)
    cl_path = os.path.join(PATH, "results")
    r_files = glob.glob(cl_path + '/*')
    for f in r_files:
        os.remove(f)


if __name__ == '__main__':
    clear_dictionaries()
    sb_scraper = SBScraper()
    container_manager = ContainerManager()

    country_url_list = sb_scraper.get_all_country_urls()
    assemble_work_packages(country_url_list)

    container_manager.start_containers(job_type='country')
    while not container_manager.finished:
        time.sleep(1)

    logging.info('Finished country packages. \n\nStarting channel packages...')

    channel_list = load_country_results(os.path.join(PATH, 'results'))
    logging.info(channel_list)
    clear_dictionaries()
    assemble_work_packages(channel_list)

    container_manager.start_containers(job_type='channel')
    while not container_manager.finished:
        time.sleep(1)

    logging.info('Finished data collection.')
