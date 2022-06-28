# dequeue and publish to channels
import redis
import time

N_BATCH = 100


def publish(batch, redis_instance, pubsub_instance):
    n_channels = len(pubsub_instance.channels.keys())
    sent_counter = 0
    with redis_instance.pipeline() as pipe:
        while batch:
            m = batch.pop()
            pipe.publish(f'{sent_counter}', m)
            if sent_counter >= n_channels:
                sent_counter = 0
            else:
                sent_counter += 1

        pipe.execute()


def dequeue(n_channels):
    r = redis.Redis(host='localhost', port=6379, db=0)
    ps = r.pubsub(ignore_subscribe_messages=True)
    if ps.channels == {}:
        for i in range(n_channels):
            ps.subscribe(f'{i}')

    batch_counter = 0
    while True:
        with r.pipeline() as pipe:
            while batch_counter < N_BATCH:
                pipe.rpop('unsent_requests')
                batch_counter += 1

            batch = pipe.execute()
            publish(batch, r, ps)
            print(f'Published {batch_counter}')
        batch_counter = 0
        time.sleep(10)


if __name__ == "__main__":
    dequeue(10)
