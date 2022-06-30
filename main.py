import os
import multiprocessing
import json
from datetime import datetime
from stopper import stopper

with open('european_countries.json') as read_file:
    list_of_cities = json.load(read_file)

channel_names = [i for i in list_of_cities]


def run_process(process):
    os.system(process)


def start_system(channel_names):
    processes = ['redis-server', 'python3.10 queuer.py', 'python3.10 leaderboard.py']
    for name in channel_names:
        processes.append(f"python3.10 listeners.py '{name}'")
    processes.append('python3.10 publisher.py')
    processes.append('python3.10 app.py')

    pool = multiprocessing.Pool(processes=len(processes))
    pool.map(run_process, processes)


if __name__ == '__main__':
    stopper(start_system(channel_names))
