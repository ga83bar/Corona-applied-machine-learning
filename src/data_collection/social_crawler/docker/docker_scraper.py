import json
import os
import time
import random
import requests
from sb_scraper_docker import SBScraper
print("python script running #########################################################")

scr_type = os.environ['JOBT']
file_id = os.environ['IDX']+".json"
print(file_id)
print(scr_type)

ip = requests.get('https://api.ipify.org').text


def read_jobs():
    with open(os.path.join("/jobs", file_id), 'r') as f:
        workload = json.load(f)
    print('### Read jobs from work file ###')
    return workload

def write_failed_jobs(jobs):
    with open(os.path.join("/jobs", "failed_"+file_id), 'w') as f:
        json.dump(jobs, f)


docker_path = '/results'

def scrape_country(job_list):
    print('### Scraping countries ###')
    scraper = SBScraper()
    results = {}
    for job in job_list:
        print('### CLOUDFLARE REQUEST ###')
        result = scraper.get_channels_by_country(job)
        results[list(result.keys())[0]] = list(result.values())[0]
        time.sleep(random.uniform(2, 4))  # Sleep so Cloudflare is not suspicious.
    print('### Scraped countries ###')
    return results

def scrape_channel(job_list):
    print('### Scraping channels ###')
    scraper = SBScraper()
    results = {}
    for job in job_list:
        result = scraper.get_channel_data(job)
        results[list(result.keys())[0]] = list(result.values())[0]
    print('### Scraped channels ###')
    return results


def write_results(results):
    with open(os.path.join('/results', file_id), 'w') as f:
        json.dump(results, f)


if __name__ == "__main__":
    jobs = read_jobs()
    try:
        if scr_type == "country":
            biggest_dict = scrape_country(jobs)
        elif scr_type == "channel":
            biggest_dict = scrape_channel(jobs)
        print('### Finished scraping ###')
        write_results(biggest_dict)

    except Exception as e:
        write_failed_jobs(jobs)
        print(e)

    


# read jobs from file

# do shit

# write results

# write failed jobs
