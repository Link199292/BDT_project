import redis
import time
import json

with open('european_countries.json') as read_file:
    list_of_cities = json.load(read_file)

channel_names = [i for i in list_of_cities]


N_BATCH = 100


def publish(batch, redis_instance, pubsub_instance):
    n_channels = len(pubsub_instance.channels.keys())
    sent_counter = 0
    with redis_instance.pipeline() as pipe:
        while batch:
            m = batch.pop()
            if m is not None:
                curr_country = eval(m)['country']
                pipe.publish(f'{curr_country}', m)
                sent_counter += 1
        pipe.execute()
        if sent_counter != 0:
            print(f'Published {sent_counter}')


def dequeue():
    r = redis.Redis(host='localhost', port=6379, db=0)
    ps = r.pubsub(ignore_subscribe_messages=True)
    if ps.channels == {}:
        for country in channel_names:
            ps.subscribe(f'{country}')

    batch_counter = 0
    while r.llen('unsent_requests') != 0:
        with r.pipeline() as pipe:
            while batch_counter < N_BATCH:
                pipe.rpop('unsent_requests')
                batch_counter += 1

            batch = pipe.execute()
            publish(batch, r, ps)
        batch_counter = 0
        time.sleep(10)


if __name__ == "__main__":
    redis_instance = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        if redis_instance.llen('unsent_requests') > 0:
            time.sleep(2)
            dequeue()
            break
