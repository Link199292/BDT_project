# dequeue and publish to channels
import redis

N_BATCH = 10000


def publish(batch, redis_instance, pubsub_instance):
    mask_channel = {idx: k for idx, k in enumerate(pubsub_instance.channels.keys())}
    sent_counter = 0
    with redis_instance.pipeline() as pipe:
        while batch:
            m = batch.pop()
            if m is None:
                break
            else:
                pipe.publish(mask_channel[sent_counter], m)
                if sent_counter == 9:
                    sent_counter = 0
                else:
                    sent_counter += 1
        pipe.execute()


def dequeue():
    r = redis.Redis(host='localhost', port=6379, db=0)
    ps = r.pubsub()
    if ps.channels == {}:
        for i in range(1, 11):
            ps.subscribe(f'ch_{i}')

    while r.llen('unsent_requests') > 0:
        batch_counter = 0
        with r.pipeline() as pipe:
            while batch_counter <= N_BATCH:
                pipe.rpop('unsent_requests')
                batch_counter += 1
            batch = pipe.execute()
            publish(batch, r, ps)


if __name__ == "__main__":
    dequeue()
