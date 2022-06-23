import os
import multiprocessing
from datetime import datetime


def run_process(process):
    os.system(process)


processes = ('redis-server', 'python3.10 queuer.py')

for n_channel in range(10):
    processes = processes + (f'python3.10 listeners.py {n_channel}', )
processes = processes + (f'python3.10 publisher.py', )


if __name__ == '__main__':

    pool = multiprocessing.Pool(processes=len(processes))
    pool.map(run_process, processes)
