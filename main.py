import redis
import json
import grequests
from index_generator import Cities, create_request

N_BATCH = 100


def exception_handler(request, exception):
    print(f"Request failed")


def send_requests(batch):
    processed = 0
    rs = (grequests.get(i, timeout=10) for i in batch)
    res = grequests.map(rs, exception_handler=exception_handler)
    text = list(map(lambda d: d.text if d else None, res))

    to_ret = []
    with r.pipeline() as pipe:
        for i, j in zip(batch, text):
            if i is None or eval(j)['status'] != 'ok':
                pipe.lpush('unsent_requests', i)
            else:
                processed += 1
                to_ret.append(j)
        pipe.execute()

    print(f"{round((processed / len(batch) * 100), 2)}% correctly processed")
    return to_ret


def batch_executor(n_batch=N_BATCH):
    batch_counter = 0
    with r.pipeline() as pipe:
        while batch_counter <= n_batch:
            pipe.rpop('unsent_requests')
            batch_counter += 1
        extracted_batch = pipe.execute()
    return send_requests(extracted_batch)


with open('european_countries.json') as read_file1, open('secrets.json') as read_file2:
    list_of_cities = json.load(read_file1)
    token = json.load(read_file2)['token']

if __name__ == "__main__":
    r = redis.RedisCluster(host='localhost', port=30001, decode_responses=True)
    r.flushdb()
    all_cities = Cities(list_of_cities)

    with r.pipeline() as pipe:
        for city in all_cities:
            curr_req = create_request(city, token)
            pipe.lpush('unsent_requests', curr_req)
        pipe.execute()

    len_monitor = r.llen('unsent_requests')
    while r.llen('unsent_requests') > 0:
        curr_len = r.llen('unsent_requests')
        if len_monitor == curr_len and curr_len < N_BATCH:
            batch_executor(n_batch=curr_len)
        else:
            batch_executor(n_batch=N_BATCH)
        len_monitor = curr_len
