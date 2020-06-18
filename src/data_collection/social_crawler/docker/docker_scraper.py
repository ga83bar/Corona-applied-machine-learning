"""reads jobs, processes jobs, writes results and failed jobs back to json"""
import json
import os
import cloudscraper

from sb_scraper_docker import SBScraper

JOB_TYPE = os.environ['JOBT']
FILE_ID = os.environ['IDX']

def read_jobs():
    with open(os.path.join("/jobs", FILE_ID), 'r') as f:
        workload = json.load(f)
    return workload


def scrape_it():
    scraper = SBScraper()
    scraper.get_channels_by_country()


def write_results(results):
    with open(os.path.join('/results', FILE_ID), 'w') as f:
        json.dump(results, f)


if __name__ == "__main__":
    jobs = read_jobs()
    #scrape_it()
    write_results(jobs)


# read jobs from file

# do shit

# write results

# write failed jobs