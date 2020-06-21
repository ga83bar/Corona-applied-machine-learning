"""!@brief ContainerManager class. Used for docker container management.
@file ContainerManager class file.
@author Martin Schuck
@author Niklas Landerer
@date 18.6.2020
"""


import threading
import os
import time
import glob
import logging
import random
import requests
import docker
import literals


logging.basicConfig(level=logging.INFO)


class ContainerManager:
    """!@brief Container Manager class to control the scraper docker containers and watch available jobs.

    This class watches the docker/jobs folder. When prompted, a limited number of docker containers starts to work on
    these jobs. The container manager creates new containers as soon as containers are finished and also reassigns the
    jobs created upon failure of a container.
    """
    def __init__(self, max_containers=10):
        """!@brief Creates a new ContainerManager object.

            @warning Docker image is not built during initialization, builds only after calling the run method!
            @param max_containers Maximum number of docker containers used to work on available jobs.
            """
        self.job_path = os.path.join(os.path.abspath(""), 'docker/jobs')
        self.results_path = os.path.join(os.path.abspath(""), 'docker/results')
        self.finished = False
        self.max_containers = max_containers
        self.docker_client = docker.from_env()
        self.containers = []
        self.known_job_list = list()
        self.watch_thread = None
        self.vpn_container = {}
        self.vpn_servers = self._query_server_list()

    def start_containers(self, job_type):
        """!@brief Starts the docker containers.

        Containers will only start with available jobs in the docker/jobs folder. Function is threaded to avoid stalling
        while containers are running. When jobs are finished, self.finished flag will be set to true. Also starts a
        watcher on the dictionary to automatically process new jobs appearing in the directory.

        @param job_type Defines the type of jobs currently present in the jobs folder. Either 'country' or 'channel'.
        """
        self.finished = False
        self.watch_thread = threading.Thread(target=self.watch_jobs, kwargs={"job_type": job_type}, daemon=True)
        self.watch_thread.start()

    def _reset(self):
        """!@brief Resets all necessary ContainerManager variables and deletes all jobs in the job folder.

         Called internally upon finishing all tasks in the jobs folder.
         @warning Will delete all files regardless of type in the jobs folder!
         """
        self.known_job_list = []
        job_files = glob.glob(self.job_path + '/*')
        for f in job_files:
            os.remove(f)

    def watch_jobs(self, job_type):
        """!@brief Watches the job folder and starts new docker containers as necessary.

        Function is meant to run threaded in the background. Checks the job folder with a frequency of 2Hz. Includes
        jobs that were assigned to a docker container into the list of known jobs. If all jobs are known and all
        containers are finished (no new jobs can be added), sets the finished flag to True. Also calls the _reset
        function.

        @param job_type Defines the type of jobs currently present in the jobs folder. Either 'country' or 'channel'.

        @note Job assignments will not be available after all jobs are completed.
        """
        while not self.finished:
            job_files = [f for f in os.listdir(self.job_path) if os.path.isfile(os.path.join(self.job_path, f))]
            job_files = [f for f in job_files if f not in self.known_job_list]
            logging.info(len(job_files))
            container_count = len(self.vpn_container)
            logging.info('container count: {}'.format(container_count))
            while len(self.vpn_container) < self.max_containers and job_files:
                file = job_files.pop()
                self.known_job_list.append(file)
                self.run(file, job_type)
                time.sleep(0.1)
            time.sleep(0.5)
            self._check_container_status()
            if not job_files and not self.vpn_container: #todo fixxx
                self.finished = True
        self._reset()

    def run(self, job_file, job_type):
        """!@brief Starts a docker container with the predefined build, the job file and the job type.

        Job files are read within the container, function only needs the job file name. Docker containers use a random
        VPN exit country. This is necessary to circumvent blocking by Cloudflare.

        @param job_file File name for the file in docker/jobs specifying the current job.
        @param job_type Defines the type of jobs currently present in the jobs folder. Either 'country' or 'channel'.
        """
        job_id = job_file.split(".")[0]
        if not self.vpn_servers:  # Refresh in case all servers are used.
            self.vpn_servers = self._query_server_list()
        server = self.vpn_servers.pop().split(".")[0]

      
        logging.info(f"building image")
        self.docker_client.images.build(path=os.path.join(os.path.abspath(""), "docker"), tag="vpn_hybrid")
        logging.info(f"image built")

        logging.info(f"starting vpn server: {server}, job_id: {job_id}")
        self.vpn_container[job_id] = self.docker_client.containers.run(image="vpn_hybrid",
                                    environment=["JOBT="+job_type, "IDX=" + job_id, "USER=patrick.kalmbach@tum.de", "PASS=LA#kYs1#o:`Z", "CONNECT=" + server, "TECHNOLOGY=NordLynx"],
                                    detach=True, tty=True, stdin_open=True,
                                    sysctls={"net.ipv4.conf.all.rp_filter": 2},
                                    privileged=True,
                                    devices=["/dev/net/tun"],
                                    name=job_id,
                                    cap_add=["NET_ADMIN", "SYS_MODULE"],
                                    volumes={self.job_path: {"bind": "/jobs/"}, self.results_path: {"bind": "/results/"}})

    def _check_container_status(self):
        old_keys = list()
        for key in self.vpn_container.keys():
            if os.path.isfile(os.path.join(self.job_path, 'failed_'+ key + '.json')) or os.path.isfile(os.path.join(self.results_path, key + '.json')):
                old_keys.append(key)
        for key in old_keys:
            self._kill_container(key)
            del(self.vpn_container[key])


    def _kill_container(self, container):
        """kills a container.
        """
        self.docker_client.containers.kill(self.vpn_container[container])

    @staticmethod
    def _query_server_list():
        """!@brief Selects a random country from predefined continents.

        Valid VPN destinations are defined in literals.
        @see literals.py

        @param vpn_destinations Dictionary of valid VPN exit points.
        @param continents List of continents the country should lie in.
        @return Returns a single country name string.
        """
        req = requests.get("https://api.nordvpn.com/v1/servers?limit=" + str(literals.NUMBER_OF_SERVERS))
        vpn_list = []

        for server in req.json():
            if server["load"] < 40:
                vpn_list.append(server["hostname"])
        random.shuffle(vpn_list)
        return vpn_list
