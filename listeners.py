import redis
import grequests
from multiprocessing import Process
import argparse
import json
import time


def exception_handler(request, exception):
    print(f"Request failed")


class Message:
    def __init__(self, message):
        self.message = eval(message['data'].decode('ASCII'))
        self.link = self.message['link']
        self.city = self.message['city']
        self.country = self.message['country']

    def __str__(self):
        return str(self.message)

    def __repr__(self):
        return str(self.message)


class Listener:
    def __init__(self, ch_n, batch_size=10):
        self.ch_number = ch_n
        self.redis_instance = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub_instance = self.redis_instance.pubsub(ignore_subscribe_messages=True)
        self.pubsub_instance.subscribe(f"{self.ch_number}")
        self.batch = []
        self.cities = []
        self.responses = None
        self.batch_size = batch_size  # in accordance with publisher N_BATCH variable

    def listen(self):
        print(f"ch_{self.ch_number} is now listening")
        while True:
            message = self.pubsub_instance.get_message()
            if message:
                current_message = Message(message)
                self.batch.append(current_message)
                self.cities.append((current_message.city, current_message.country, current_message.link))
                if len(self.batch) >= self.batch_size:
                    self.send_requests()
                    self.batch = []
            else:
                time.sleep(0.001)

    def send_requests(self):
        rs = (grequests.get(i.link, timeout=5) for i in self.batch)
        res = grequests.imap(rs, exception_handler=exception_handler)
        self.responses = list(map(lambda d: d.text if d else None, res))

        print(self.responses)

        for idx, r in enumerate(self.responses):
            diz = {'city': self.cities[idx][0], 'country': self.cities[idx][1], 'link': self.cities[idx][-1]}
            if r is not None:
                curr_req = json.loads(r)
                if curr_req['status'] == 'ok':
                    self.redis_instance.zadd('leaderboard', {self.cities[idx][0]: int(curr_req['data']['aqi'])})
            else:
                self.redis_instance.lpush('unsent_requests', json.dumps(diz))
                print(f'SENDING BACK: {self.cities[idx][0]}')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('n', help='channel name')
    args = parser.parse_args()

    Listener(ch_n=args.n).listen()
