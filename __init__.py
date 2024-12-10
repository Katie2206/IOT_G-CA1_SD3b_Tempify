import json
import time

import os
import pathlib
import requests

from flask import Flask, session, redirect, request, abort, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from .config import config

from . import my_db

db = my_db.db

app = Flask(__name__)
app.secret_key = config.get("APP_SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

GOOGLE_CLIENT_ID = (
    config.get("GOOGLE_CLIENT_ID")
)
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, ".client_secret.json")


flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="https://www.tempify.live/callback",
)

alive = 0
data = {}


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()

    return wrapper


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/protected_area")
@login_is_required
def protected_area():
    my_db.add_user_and_login(session['google_id'], session['username'], session['email_address'])
    return render_template("protected_area.html", user_id=session['google_id'], online_users=my_db.view_all_users(), admin_id=config.get('GOOGLE_ADMIN_ID'))


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/logout")
def logout():
    my_db.user_logout(session['google_id'])
    session.clear()
    return redirect("/")


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    Token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=Token_request, audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["username"] = id_info.get("name")
    session["email_address"] = id_info.get("email")
    print(session["google_id"])
    print(session["username"])
    return redirect("/protected_area")


@app.route('/grant-<User_ID>-<read>-<write>', methods=["POST"])
def grant_access(User_ID, read, write):
    if session['google_id']:
        if session['google_id'] == config.get('GOOGLE_ADMIN_ID'):
            print(f"Admin granting {User_ID}-{read}-{write}")
            my_db.add_user_permission(User_ID, read, write)
            if read=="true" and write=="true":
                Token = pb.grant_read_write_access(User_ID)
                my_db.add_token(User_ID, Token)
                access_response = {'Token': Token, 'cipher_key': pb.cipher_key, 'uuid':User_ID}
                return json.dumps(access_response)
            elif read == True and write == True:
                Token = pb.grant_read_write_access(User_ID)
                my_db.add_token(User_ID, Token)
                return json.dumps(Token)
            elif read=="true" and write=="false":
                Token = pb.grant_read_access(User_ID)
                my_db.add_token(User_ID, Token)
                access_response = {'Token': Token, 'cipher_key': pb.cipher_key, 'uuid':User_ID}
                return json.dumps(access_response)
            elif read == True and write == False:
                Token = pb.grant_read_write_access(User_ID)
                my_db.add_token(User_ID, Token)
                return json.dumps(Token)
            elif read=="false" and write=="true":
                Token = pb.grant_write_access(User_ID)
                my_db.add_token(User_ID, Token)
                access_response = {'Token': Token, 'cipher_key': pb.cipher_key, 'uuid':User_ID}
                return json.dumps(access_response)
            elif read == False and write == True:
                Token = pb.grant_read_write_access(User_ID)
                my_db.add_token(User_ID, Token)
                return json.dumps(Token)
            else:
                #remove existing Token from database
                my_db.delete_revoked_token(User_ID)
                access_response = {'Token':123, 'cipher_key':"Thiswillnotwork", 'uuid':User_ID}
                return json.dumps(access_response)
        else:
            print(f"Non-admin attempting to grant privileges {User_ID}-{read}-{write}")
            my_db.add_user_permission(User_ID, read, write)
            Token = my_db.get_token(User_ID)
            if Token is not None:
                timestamp, uuid, read,write = pb.parse_token(Token)
                current_time = time.time
                if(timestamp+(ttl*60)) - current_time > 0:
                    print("Token is still valid")
                    access_response = {'Token': Token, 'cipher_key': pb.cipher_key, 'uuid':User_ID}
                    return json.dumps(access_response)
                else:
                    print("Token refresh needed")
                    if read and write:
                        Token = pb.grant_read_write_access(User_ID)
                        my_db.add_token(User_ID, Token)
                        access_response = {'Token': Token, 'cipher_key': pb.cipher_key, 'uuid':User_ID}
                        return json.dumps(access_response)
                    elif read:
                        Token = pb.grant_read_access(User_ID)
                        my_db.add_token(User_ID, Token)
                        access_response = {'Token': Token, 'cipher_key': pb.cipher_key, 'uuid':User_ID}
                        return json.dumps(access_response)
                    elif write:
                        Token = pb.grant_write_access(User_ID)
                        my_db.add_token(User_ID, Token)
                        access_response = {'Token': Token, 'cipher_key': pb.cipher_key, 'uuid':User_ID}
                        return json.dumps(access_response)
                    else:
                        access_response = {'Token':123, 'cipher_key':"Thiswillnotwork", 'uuid':User_ID}
                        return json.dumps(access_response)



@app.route('/get_user_token', methods=['POST'])
def get_user_token():
    User_ID = session['google_id']
    Token = my_db.get_token(User_ID)
    if Token is not None:
        Token = get_or_refresh_token(Token)
        token_response = {'Token': Token, 'cipher_key': pb.cipher_key, 'uuid':User_ID}
    else:
        token_response = {'Token':123, 'cipher_key':"Thiswillnotwork", 'uuid':User_ID}
    return json.dumps(token_response)


def get_or_refresh_token(Token):
    timestamp, ttl, uuid, read, write = pb.parse_token(Token)
    current_time = time.time()
    if(timestamp+(ttl*60)) - current_time > 0:
        return Token
    else:
        #the Token has expired
        return grant_access




@app.route("/main")
def main():
    return render_template("main.html")

# @app.route("/keep_alive")
# def keep_alive():
#     global alive, data
#     alive += 1
#     keep_alive_count = str(alive)
#     data["keep_alive"] = keep_alive_count
#     parsed_json = json.dumps(data)
#     print(parsed_json)
#     return str(parsed_json)

              
if __name__ == "__main__":
   app.run()
