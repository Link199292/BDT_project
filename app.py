from unicodedata import name
from flask import Flask, render_template

app = Flask(__name__)

# Adding dummy tuples as the original code 
# could not be run on my system without errors.

headings = ("City_Name", "AQI", "Ranking")

data = (
    ("Trento", "15", "01"),
    ("Dublin", "27", "02"),
    ("Roma", "49", "03"),
    ("Toulouse", "108", "04"),
    ("Paris", "500", "05")
)

@app.route("/")
def table():
    return render_template("index.html", headings=headings, data=data)

if __name__=='__main__':
    app.run(debug=True,port=5001)