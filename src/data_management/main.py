"""
This class serves as the CLI access point to intelligently and selectively access requested data.
The User has the option of receiving ONLY the data they want, or all the data available to them.
Please use this CLI as the starting point for all future expansions.
"""


import asyncio
import sys
from asynccmd import Cmd
from data_collection import DataCollection as dc

# Prompts
INTRO = 'Welcome to the Data Management Shell.   Type help or ? to list commands.\n'
PROMPT = '---ENTER COMMAND: '


class DataShell(Cmd):
    def __init__(self, mode, intro, prompt):
        super().__init__(mode=mode)
        self.intro = 'Welcome to the Data Management Shell.   Type help or ? to list commands.\n'
        self.prompt = '---ENTER COMMAND: '
        self.loop = None

    def do_tasks(self, arg):
        """"""
        for task in asyncio.Task.all_tasks(loop=self.loop):
            print(task)

    # ----- All actionable commands -----
    def do_req_covid_data_all(self, arg):
        """ Request and update current hardware_io information"""
        self.loop.create_task()

    def do_req_covid_data_world(self, arg):
        """ Request and update current hardware_io information"""
        self.loop.create_task()

    def do_req_covid_data_countries(self, arg):
        """ Request and update current hardware_io information"""
        self.loop.create_task()

    def do_terminate(self, arg):
        """ Stop the shell and exit:  terminate"""
        print("CLI terminated\n")
        self.loop.stop()
        return True

    def start(self, loop=None):
        self.loop = loop
        super().cmdloop(loop)

    async def get_covid_data(self, countries, save_frame=False, do_plot=False):
        """ Access point for the async CLI to access COVID API """
        dc.get_covid_data(countries, save_frame, do_plot)
        return True


def parse(arg):
    return tuple(map(int, arg.split()))


if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    mode = "Run"
else:
    loop = asyncio.get_event_loop()
    mode = "Reader"


cmd = DataShell(mode=mode, intro=INTRO, prompt=PROMPT)
cmd.start(loop)

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.stop()