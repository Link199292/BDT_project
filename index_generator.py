import random


class Cities:
    def __init__(self, list_of_cities):
        self.cities = [city for country in list_of_cities for city in list_of_cities[country]]
        random.shuffle(self.cities)
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
            return self.cities[self._index]

    def __getitem__(self, index):
        if index <= len(self.cities):
            return self.cities[index]
        else:
            raise IndexError