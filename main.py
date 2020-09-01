import os
from pathlib import Path
import threading
import src.webinterface.backend.api as backend


def main():
    '''Main function'''
   
    print("\n---Starting backend---")
    backend.main()


if __name__ == '__main__':
    main()
