import os
import src.webinterface.backend.api as backend


def main():
    '''Main function'''

    # Start the backend
    # TODO: Start it in a seperate thread
    backend.main()
    # Start the npm server for the frontend
   

if __name__ == '__main__':
    main()
