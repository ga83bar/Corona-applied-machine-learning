import json
import os
import requests
#from sb_scraper_docker import SBScraper
print("python script running #########################################################")

scr_type = os.environ['JOBT']
file_id = os.environ['IDX']+".json"
print(file_id)
print(scr_type)

ip = requests.get('https://api.ipify.org').text


def read_jobs():
    with open(os.path.join("/jobs", file_id), 'r') as f:
        workload = json.load(f)
    return workload

docker_path = '/results'

def scrape_it():
    scraper = SBScraper()
    scraper.get_channels_by_country()


def write_results(results):
    with open(os.path.join('/results', file_id), 'w') as f:
        json.dump(results, f)


if __name__ == "__main__":
    jobs = read_jobs()
    # scrape_it()
    write_results(ip)


# read jobs from file

# do shit

# write results

# write failed jobs
