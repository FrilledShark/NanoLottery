from flask import Flask, render_template
from modules.database import Ticket, Lottery, tables, db

import os, json  # Reading config file
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'config.json')
with open(filename, 'r') as file:
    config = json.load(file)



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()