import json
import html

european_countries = {}

with open('euro-countries.json') as r:
    for country in json.load(r):
        european_countries[country['name']] = []

with open('cities.json') as r:
    for city in json.load(r):
        curr_country = city['country_name']
        if curr_country in european_countries:
            city_name = city['name']
            city_lat = city['latitude']
            city_lon = city['longitude']

            to_add = {'city': city_name,
                      'latitude': city_lat,
                      'longitude': city_lon}

            european_countries[curr_country].append(to_add)

with open('european_countries.json', 'w') as w:
    json.dump(european_countries, w, indent=4)

