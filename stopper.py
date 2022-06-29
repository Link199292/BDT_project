import time
import os


def stopper(main_function, hrs=24):
    while True:
        main_function
        time.sleep(60 * 60 * hrs)