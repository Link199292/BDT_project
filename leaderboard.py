import pymongo
from pymongo import MongoClient
import redis
import time


class MongoDB:
    def __init__(self):
        self.redis_instance = redis.Redis(host='localhost', port=6379, db=0)
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['BDT_database']
        self.collection_instance = None
        self.collection_name = None

    def listen(self):
        while self.redis_instance.llen('unsent_requests') > 0 or self.redis_instance.llen('for_mongo') > 0:
            if self.redis_instance.llen('for_mongo') > 0:  # check for the existence of the queue
                current_city = eval(self.redis_instance.rpop('for_mongo'))
                self.insert(current_city)

    def insert(self, city):
        self.collection_name = city['country']
        self.collection_instance = self.db[self.collection_name]
        cursor = self.collection_instance.find_one({'city': city['city']})
        if cursor is None:
            self.collection_instance.insert_one(city)
        else:
            prev_update = cursor.get('last_update')
            if prev_update != city['last_update']:
                self.collection_instance.find_one_and_update({'city': city['city']}, {'$set': {'aqi': city['aqi'], 'last_update': city['last_update']}})
        self.populate_leaderboard(city)

    def populate_leaderboard(self, element):
        if element['aqi'] != '-':
            self.redis_instance.zadd(f"{element['country']}", {element['city']: element['aqi']})


if __name__ == '__main__':
    database = MongoDB()
    time.sleep(10)
    while True:
        if database.redis_instance.llen('unsent_requests') > 0:
            database.listen()
            break
