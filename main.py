import os
import multiprocessing
from datetime import datetime

def run_process(process):
    os.system(process)


if __name__ == '__main__':

    processes = ('redis-server',
                 'python3.10 queuer.py',
                 'python3.10 listeners.py 0',
                 'python3.10 listeners.py 1',
                 'python3.10 listeners.py 2',
                 'python3.10 listeners.py 3',
                 'python3.10 listeners.py 4',
                 'python3.10 listeners.py 5',
                 'python3.10 listeners.py 6',
                 'python3.10 listeners.py 7',
                 'python3.10 listeners.py 8',
                 'python3.10 listeners.py 9',
                 'python3.10 publisher.py')

    pool = multiprocessing.Pool(processes=len(processes))
    pool.map(run_process, processes)