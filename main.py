import redis
import requests
import json
from index_generator import Cities, City, create_request

with open('european_countries.json') as read_file1, open('secrets.json') as read_file2:
    list_of_cities = json.load(read_file1)
    token = json.load(read_file2)['token']

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    all_cities = Cities(list_of_cities)
    for city in all_cities:
        curr_req = create_request(city, token)
        r.rpush('unsent_requests', curr_req)
    curr_batch = r.lpop('unsent_requests', 100)