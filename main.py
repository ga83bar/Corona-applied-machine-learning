import os
from pathlib import Path
import threading
import src.webinterface.backend.api as backend


def start_frontend():
    relative_path = Path.cwd()
    print(relative_path)

    # Start the npm server for the frontend

    path_to_frontend = Path("/src/webinterface/clean-frontend")
    print(str(relative_path) + str(path_to_frontend))
    total_path = Path(str(relative_path) + str(path_to_frontend))
    cmd = 'cmd /k "cd {} && npm run serve"'.format(total_path)
    print(cmd)
    os.system(cmd)


def main():
    '''Main function'''

    print("\n---Starting frontend---")
    frontend_thread = threading.Thread(target= start_frontend)
    frontend_thread.start()
    # Start the backend
    # TODO: Start it in a seperate thread
    print("\n---Starting backend---")
    backend.main()


if __name__ == '__main__':
    main()
