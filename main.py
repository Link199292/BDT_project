import os
import multiprocessing
from datetime import datetime


def run_process(process):
    os.system(process)


def start_system(n_listeners):
    processes = ['redis-server', 'python3.10 queuer.py']
    for n_channel in range(n_listeners):
        processes.append(f'python3.10 listeners.py {n_channel}')
    processes.append('python3.10 publisher.py')
    processes = tuple(processes)

    pool = multiprocessing.Pool(processes=len(processes))
    pool.map(run_process, processes)


if __name__ == '__main__':
    start_system(10)
