import json
import requests

mask = {range(0, 51): 0,
        range(51, 101): 1,
        range(101, 151): 2,
        range(151, 201): 3,
        range(201, 301): 4,
        range(301, 1000): 5}


class City:
    def __init__(self, diz):
        self.name = diz['city']
        self.latitude = diz['latitude']
        self.longitude = diz['longitude']


class Cities:
    def __init__(self, list_of_cities):
        self.cities = [city for country in list_of_cities for city in list_of_cities[country]]
        self._index = -1

    def __len__(self):
        return len(self.cities)

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index >= len(self.cities):
            self._index = -1
            raise StopIteration
        else:
            return City(self.cities[self._index])

    def __getitem__(self, index):
        if index <= len(self.cities):
            return City(self.cities[index])
        else:
            raise IndexError


def create_request(city, token):
    link = f"https://api.wagi.info/feed/geo{city['latitude']};{city['longitude']}/?token={token}"
    return link
