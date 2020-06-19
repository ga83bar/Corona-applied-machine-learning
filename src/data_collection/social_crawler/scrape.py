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


from sb_scraper import SBScraper
import json
import os
import shortuuid
from container_manager import ContainerManager
import time


PACKAGE_SIZE = 50
PATH = os.path.join(os.path.abspath(""), 'docker')


def assemble_work_packages(url_list):
    """!@brief Creates several work packages from a list of urls that need to be scraped and saves them.

    Slices the url list into multiple packages. Maximum package size as defined in PACKAGE_SIZE. Single work packages
    get saved into the docker/jobs folder as json files with a unique file name.

    @param url_list List of urls that need to be scraped.
    """
    work_packages = [url_list[x:x + PACKAGE_SIZE] for x in range(0, len(url_list), PACKAGE_SIZE)]
    for package in work_packages:
        with open(os.path.join(PATH, 'jobs', str(shortuuid.uuid()) + '.json'), 'w') as f:
            json.dump(package, f)


def load_country_results(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    channel_url_list = list()
    for file in files:
        with open(os.path.join(path, file), 'r') as f:
            country_dict = json.load(f)
            channel_url_list.extend(list(country_dict.values())[0])
    return channel_url_list


if __name__ == '__main__':
    sb_scraper = SBScraper()
    container_manager = ContainerManager()

    country_url_list = sb_scraper.get_all_country_urls()
    assemble_work_packages(country_url_list)

    container_manager.start_containers(job_type='country')
    while not container_manager.finished:
        time.sleep(1)

    print('Finished country packages. \n\nStarting channel packages...')

    channel_list = load_country_results(os.path.join(PATH, 'results'))
    assemble_work_packages(channel_list)

    container_manager.start_containers(job_type='channel')
    while not container_manager.finished:
        time.sleep(1)

    print('Finished data collection.')
