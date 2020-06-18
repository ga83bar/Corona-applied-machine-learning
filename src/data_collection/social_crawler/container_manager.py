import threading
import os
import docker


class ContainerManager:

    def __init__(self, max_containers=20):
        self.path = os.path.join(os.path.abspath(""), 'docker\\jobs')
        self.run_tread = threading.Thread(target=self.watch_jobs, daemon=True)
        self.finished = False
        self.max_containers = max_containers
        self.docker_client = docker.from_env()
        self.known_job_list = list()

    def start_containers(self):
        self.finished = False
        self.run_tread.start()

    def watch_jobs(self):
        while not self.finished:
            job_files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
            container_count = len(self.docker_client.containers.list())
            if not container_count > self.max_containers and job_files:
                for file in job_files:
                    if file.exists(file + 'dockerout'):
                        delete
            self.finished = True
        self._reset()

    def run(self):


