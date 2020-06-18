"""reads jobs, processes jobs, writes results and failed jobs back to json"""
import json
import os
import cloudscraper

JOB_TYPE = os.environ['JOBT']
FILE_ID = os.environ['IDX']

rsp = {'type': JOB_TYPE, 'file_id': FILE_ID}

docker_path = '/results'

with open(os.path.join(docker_path, FILE_ID + '.json'), 'w') as f:
    json.dump(rsp, f)


# read jobs from file

# do shit

# write results

# write failed jobs