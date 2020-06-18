from sb_scraper import SBScraper
import json
import os
import uuid
from container_manager import ContainerManager
import time


PACKAGE_SIZE = 50
PATH = os.path.join(os.path.abspath(""), 'docker')


def assemble_work_packages(url_list, job_type):
    work_packages = [url_list[x:x + PACKAGE_SIZE] for x in range(0, len(url_list), PACKAGE_SIZE)]
    for package in work_packages:
        with open(os.path.join(PATH, 'jobs', str(uuid.uuid4()) + '.json'), 'w') as f:
            json.dump(package, f)


if __name__ == '__main__':
    sb_scraper = SBScraper()
    container_manager = ContainerManager()

    country_url_list = sb_scraper.get_all_country_urls()
    assemble_work_packages(country_url_list, 'country')

    container_manager.start_containers(job_type='country')
    while not container_manager.finished:
        time.sleep(1)

    print('Finished country packages. \n\nStarting channel packages...')

    channel_list = load_files(os.path.join(PATH, 'results'))
    assemble_work_packages(channel_list, 'channel')

    container_manager.start_containers(job_type='channel')
    while not container_manager.finished:
        time.sleep(1)

    print('Finished data collection.')
