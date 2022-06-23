import redis
import grequests
import time
from multiprocessing import Process
import argparse


def exception_handler(request, exception):
    print(f"Request failed")


class Listener:
    def __init__(self, ch_n, batch_dim=100):
        self.batch_dim = batch_dim
        self.ch_number = ch_n
        self.batch = []
        self.redis_instance = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub_instance = self.redis_instance.pubsub()
        self.pubsub_instance.subscribe(f'ch_{self.ch_number}')

    def listen(self):
        print(f'ch_{self.ch_number} is listening')
        while True:
            message = self.pubsub_instance.get_message()
            if message:
                self.batch.append(message['data'])
                if len(self.batch) >= self.batch_dim:
                    self._send_requests()
            else:
                time.sleep(0.001)

    def _send_requests(self):
        rs = (grequests.get(i, timeout=10) for i in self.batch)
        res = grequests.map(rs, exception_handler=exception_handler)
        text = list(map(lambda d: d.text if d else None, res))

        # TODO here the API response has to be taken, the values should be subsetted taking just the AQI value and the
        # name/coords of the city so to make it possible to generate an ordered list. After that, the results should be
        #represented in some way: website, dashboard, map, ...

        # TODO also here, it should be checked whether a request has been failed to be retrieved, in that case it should
        # be reinserted into the 'unsent_requests' queue
        self.batch = []


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('n', help='channel name')
    args = parser.parse_args()

    Listener(ch_n=args.n, batch_dim=100).listen()
