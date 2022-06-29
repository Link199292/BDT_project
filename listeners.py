import redis
import requests
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
    def __init__(self, ch_n, batch_size=100):
        self.ch_number = ch_n
        self.redis_instance = redis.Redis(host='localhost', port=6379, db=0)
        self.pubsub_instance = self.redis_instance.pubsub(ignore_subscribe_messages=True)
        self.pubsub_instance.subscribe(f"{self.ch_number}")
        self.batch = []
        self.cities = []
        self.responses = []
        self.batch_size = batch_size  # in accordance with publisher N_BATCH variable

    def listen(self):
        print(f"{self.ch_number} is now listening")
        while self.redis_instance.llen('unsent_requests') or self.pubsub_instance.get_message() is not None:
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
        while self.batch:
            current_city = self.batch.pop()
            response = requests.get(current_city.link)
            response_json = eval(response.text)
            if response_json['status'] == 'ok':
                curr_aqi = response_json['data']['aqi']
                last_update = response_json['data']['debug']['sync']
                to_insert = {'city': current_city.city,
                             'country': current_city.country,
                             'aqi': curr_aqi,
                             'last_update': last_update}
                self.redis_instance.lpush('for_mongo', json.dumps(to_insert))
            else:
                print(f'sending back {current_city.city}')
                self.redis_instance.lpush('unsent_requests', json.loads(current_city))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('n', help='channel name')
    args = parser.parse_args()

    listener = Listener(ch_n=args.n, batch_size=10)
    while True:
        if listener.redis_instance.llen('unsent_requests') > 0:
            listener.listen()
            break

