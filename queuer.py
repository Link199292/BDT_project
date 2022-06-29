import redis
import json
from index_generator import Cities


def create_request(city, token):
    return f"https://api.waqi.info/feed/geo:{city['latitude']};{city['longitude']}/?token={token}"


with open('european_countries.json') as read_file1, open('secrets.json') as read_file2:
    list_of_cities = json.load(read_file1)
    token = json.load(read_file2)['token']

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushall()  # empties everything, remember to remove it, otherwise at each restart the db is flushed
    ps = r.pubsub()

    all_cities = Cities(list_of_cities)


    city_counter = 0
    with r.pipeline() as pipe:
        for city in all_cities:
            curr_req = create_request(city, token)
            diz = {'city': city['city'], 'country': city['country'], 'link': curr_req}
            pipe.lpush('unsent_requests', json.dumps(diz))
            city_counter += 1
        pipe.execute()
        print(f'{city_counter} elements inserted into queue')
