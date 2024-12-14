import json
from flask_sqlalchemy import SQLAlchemy

import os
import pathlib

from flask import Flask, session, redirect, render_template
from .config import config

from . import my_db

db = my_db.db

app = Flask(__name__)
app.secret_key = config.get("APP_SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
Plant = my_db.Plant
Soil = my_db.Soil
Temperature = my_db.Temperature
Humidity = my_db.Humidity

alive = 0
data = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/protected_area")
def protected_area():
    return render_template("protected_area.html")


@app.route("/main")
def main():
    plant_data = db.session.query(Plant).all()
    return render_template("main.html", plants = plant_data)


@app.route("/temp")
def temp():
    temp_data = db.session.query(Temperature).all()
    return render_template("temp.html", temp = temp_data)

@app.route("/soilTemp")
def soilTemp():
    soil_data = db.session.query(Soil).all()
    return render_template("soilTemp.html", soil = soil_data)

@app.route("/humidity")
def humidity():
    humidity_data = db.session.query(Humidity).all()
    return render_template("humidity.html", humidity = humidity_data)


@app.route("/keep_alive")
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data["keep_alive"] = keep_alive_count
    parsed_json = json.dumps(data)
    print(parsed_json)
    return str(parsed_json)

            
# @app.route('/get_plant_token', methods=['POST'])
# def get_plant_token():
#     Plant_ID = 1
#     Token = my_db.get_token(Plant_ID)
#     if Token is not None:
#         Token = get_or_refresh_token(Token)
#         token_response = {'Token': Token, 'cipher_key': pb.cipher_key}
#     else:
#         token_response = {'Token':123, 'cipher_key':"Thiswillnotwork"}
#     return json.dumps(token_response)


# def get_or_refresh_token(Token):
#     timestamp, ttl = pb.parse_token(Token)
#     current_time = time.time()
#     if(timestamp+(ttl*60)) - current_time > 0:
#         return Token
#     else:
#         return Token
    

if __name__ == "__main__":
   app.run()
