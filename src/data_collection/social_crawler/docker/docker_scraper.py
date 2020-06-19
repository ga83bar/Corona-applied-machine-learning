import json
import os
from sb_scraper_docker import SBScraper

scr_type = os.environ['JOBT']
file_id = os.environ['IDX']


def read_jobs():
    with open(os.path.join("/jobs", FILE_ID), 'r') as f:
        workload = json.load(f)
    return workload

docker_path = '/results'

def scrape_it():
    scraper = SBScraper()
    scraper.get_channels_by_country()


def write_results(results):
    with open(os.path.join('/results', FILE_ID), 'w') as f:
        json.dump(results, f)


if __name__ == "__main__":
    jobs = read_jobs()
    # scrape_it()
    write_results(jobs)


# read jobs from file

# do shit

# write results

# write failed jobs
