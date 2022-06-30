from unicodedata import name
from flask import Flask, render_template
from pymongo import MongoClient
from turbo_flask import Turbo
import json
import threading
import time


with open('euro-countries.json') as read_file:
    countries = json.load(read_file)
countries = [i['name'] for i in countries]

client = MongoClient('mongodb://localhost:27017/')
db = client['BDT_database']


def update_database():
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
    print(curr_data)
    return curr_data[:51]


app = Flask(__name__)
turbo = Turbo(app)

headings = ("Country", "City_Name", "AQI")

prev_data = update_database()

@app.route("/")
def table():
    return render_template("index.html", headings=headings, data=prev_data)


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load()).start()


def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            data = update_database()
            turbo.push(turbo.replace(render_template('index.html', headings=headings, data=prev_data), target=data))


if __name__ == '__main__':
    app.run(debug=False, port=5001)
