import redis
import json
import grequests
from index_generator import Cities, create_request

N_BATCH = 100

with open('european_countries.json') as read_file1, open('secrets.json') as read_file2:
    list_of_cities = json.load(read_file1)
    token = json.load(read_file2)['token']

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushall()  # empties everything, remember to remove it, otherwise at each restart the db is flushed
    ps = r.pubsub()

    all_cities = Cities(list_of_cities)

    with r.pipeline() as pipe:
        for city in all_cities:
            curr_req = create_request(city, token)
            pipe.lpush('unsent_requests', curr_req)
        res = pipe.execute()
    print(f'{len(res)} elements inserted into queue')
