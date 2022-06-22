import redis
import json
import grequests
from index_generator import Cities, create_request


def exception_handler(request, exception):
    print(f"Request failed")


def send_requests():
    processed = 0
    rs = (grequests.get(i, timeout=10) for i in batch)
    res = grequests.map(rs, exception_handler=exception_handler)
    text = list(map(lambda d: d.text if d else None, res))
    for i, j in zip(res, text):
        if i.status_code == 200:
            processed += 1
    to_ret = []
    for i in text:
        if i is None:
            r.lpush('unsent_requests', i)
        else:
            to_ret.append(i)

    print(f"{round((processed / len(batch) * 100), 2)}% correctly processed")
    return to_ret


with open('european_countries.json') as read_file1, open('secrets.json') as read_file2:
    list_of_cities = json.load(read_file1)
    token = json.load(read_file2)['token']

batch_counter = 0
batch = []

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushdb()
    all_cities = Cities(list_of_cities)
    for city in all_cities:
        curr_req = create_request(city, token)
        r.lpush('unsent_requests', curr_req)

    while r.llen('unsent_requests') != 0:
        if batch_counter >= 100:
            print('reached 100 requests')
            batch_counter = 0
            for link in batch:
                x = link.decode('ASCII')
                a, b = x.split('geo')
                x = f"{a}geo{b}"
            result = send_requests()
            # reinsert into Redis and sort (use Redis ordered list)
            batch = []
        else:
            x = r.rpop('unsent_requests')
            batch.append(x)
            batch_counter += 1
