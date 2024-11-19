from flask import Flask, session, redirect, request, abort, render_template
import os
import pathlib
import requests
import json
import time


from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests


app = Flask(__name__)

alive = 0
data = {}

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/protected_area")
def protected_area():
    return "Protected Area <a href = '/logout'><button>Logout</button></a>"


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/callback")
def callback():
    Flow.fetch_token(authorization_response = request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = Flow.credentials
    request_session = requests.session
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session = cached_session)

    id_info = id_token.verify_token(
        id_token = credentials.id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    print(session["google_id"])
    print(session["name"])
    return redirect("/protected_area")
    

if __name__ == "__main__":
    app.run(debug=True)