"""quick and dirty script that builds and runs docker containers for social scraper"""
import argparse
import os
import docker

PATH = os.path.abspath("")

def build_container(client):
    """builds image from Dockerfile if not already built"""
    client.images.build(path=os.path.join(os.path.abspath(""), "docker"), tag="scrape_light")

def start_container(client, work_package, load_saved):
    """uses docker client to start a container"""
    package_path = os.path.join(PATH, "/work_packages")

    client.containers.run(image="scrape_light",
                          environment=["PACKAGE="+work_package, "LOAD_FILE=" + load_saved, "USERNAME=patrick.kalmbach@tum.de", "PASSWORD=LA#kYs1#o:`Z"],
                          detach=True, tty=True, stdin_open=True,
                          sysctls={"net.ipv4.conf.all.rp_filter": 2},
                          privileged=True,
                          devices=["/dev/net/tun"],
                          name="scrape_" + str(work_package),
                          cap_add=["NET_ADMIN", "SYS_MODULE"],
                          volumes={package_path: {"bind": "/work_packages"}})

if __name__ == "__main__":
    client = docker.from_env()
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--package_id', default=0, help='provide id for the work package, comma separated if multiple')
    parser.add_argument('--load_quicksave', default="no", help='wanna load? -> yes/no')
    args = parser.parse_args()
    packages = args.package_id.split(",")

    build_container(client)

    for package in packages:
        start_container(client, int(package), args.load_quicksave)
