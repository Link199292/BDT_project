import json

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
                      'latitude': round(float(city_lat), 1),
                      'longitude': round(float(city_lon), 1)}

            european_countries[curr_country].append(to_add)

to_del = []

for i in european_countries:
    if not european_countries[i]:
        to_del.append(i)

for i in to_del:
    del european_countries[i]

with open('european_countries.json', 'w') as w:
    json.dump(european_countries, w, indent=4)
