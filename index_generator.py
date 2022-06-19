import json
import requests

mask = {range(0, 51): 0,
        range(51, 101): 1,
        range(101, 151): 2,
        range(151, 201): 3,
        range(201, 301): 4,
        range(301, 1000): 5}

token = '68b47eb3b1f697ab426e102486f11c68fb3dc5b1'


with open('european_countries.json') as read_file:
    all_cities = json.load(read_file)


for country in all_cities:
    print(f'Currently: {country}')
    for city in all_cities[country]:
        curr_city = city['city']
        curr_lat = city['latitude']
        curr_lon = city['longitude']
        try:
            response = requests.get(f'https://api.waqi.info/geo:{curr_lat};{curr_lon}/?token={token}')
            print(response.status)
        except:
            print(country, city, curr_lat, curr_lon)