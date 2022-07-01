from unicodedata import name
from flask import Flask, render_template
from pymongo import MongoClient
import json


with open('euro-countries.json') as read_file:
    countries = json.load(read_file)
countries = [i['name'] for i in countries]

client = MongoClient('mongodb://localhost:27017/')
db = client['BDT_database']


app = Flask(__name__)

headings = ("Country", "City_Name", "AQI")


def update_database():
    while True:
        curr_data = []
        for country in countries:
            current_collection = list(db[country].find())
            for city in current_collection:
                curr_country = city['country']
                curr_city = city['city']
                curr_aqi = city['aqi']
                if curr_aqi != '-':
                    curr_data.append((curr_country, curr_city, curr_aqi))
        curr_data.sort(key=lambda x: x[-1])
        return curr_data[:51]


@app.route("/")
def table():
    return render_template("index.html", headings=headings, data=update_database())


if __name__ == '__main__':
    app.run(debug=False, port=5001)
