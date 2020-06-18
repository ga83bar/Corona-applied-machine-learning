import threading
import os
import docker
import time
import logging
import literals
import random


class ContainerManager:

    def __init__(self, max_containers=20):
        self.job_dir = os.path.join(os.path.abspath(""), 'docker\\jobs')
        self.results_dir = os.path.join(os.path.abspath(""), 'docker\\results')
        self.finished = False
        self.max_containers = max_containers
        self.docker_client = docker.from_env()
        self.containers = []
        self.known_job_list = list()
        self.watch_thread = None

    def start_containers(self, job_type):
        self.finished = False
        self.watch_thread = threading.Thread(target=self.watch_jobs, kwargs={"job_type": job_type}, daemon=True)
        self.watch_thread.start()

    def _reset(self):
        self.known_job_list = []

    def watch_jobs(self, job_type):
        print('watch thread started')
        while not self.finished:
            job_files = [f for f in os.listdir(self.job_dir) if os.path.isfile(os.path.join(self.job_dir, f))]
            job_files = [f for f in job_files if f not in self.known_job_list]
            container_count = len(self.docker_client.containers.list())
            print('container count: {}'.format(container_count))
            while not container_count > self.max_containers and job_files:
                file = job_files.pop()
                self.known_job_list.append(file)
                self.run(file, job_type)
            time.sleep(0.5)
        self.finished = True
        self._reset()

    def run(self, job_file, job_type):
        print('RUN CALLED')
        print('JOB FILE: \n{}'.format(job_file))
        self.docker_client.images.build(path="./docker/", tag="scrape")
        logging.info(f"Image built.")
        country = self._choose_a_country(literals.VPN_DESTINATIONS, ["europe"])
        self.docker_client.containers.run(image="scrape", auto_remove=True,
                                          environment=["JOBT=" + country, "IDX=" + job_file, "ACTIVATION_CODE=EH5VWAJ5HRM7T5XPSY392IB", "SERVER=ITALY"],
                                          detach=True, tty=True,
                                          privileged=True,
                                          devices=["/dev/net/tun"],
                                          cap_add=["NET_RAW", "NET_ADMIN"],
                                          volumes={self.job_dir: {"bind": "/jobs/"}, self.results_dir: {"bind": "/results/"}}
                                          )
        logging.info("Image built.")

    @staticmethod
    def _choose_a_country(vpn_destinations, continents):
        """selects a random country within the specified continents"""
        candidates = []
        for continent in continents:
            candidates.append(vpn_destinations[continent])
        candidates = [item for sublist in candidates for item in sublist]
        return random.choice(candidates)