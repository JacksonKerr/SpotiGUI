# -*- coding: utf-8 -*-

from flask import Flask, redirect, request
import requests
import sys
import os
import base64
import json
import socket
from threading import *
app = Flask(__name__)

@app.route('/')
def main():
    permissions = ("user-read-playback-position%20"
                    + "user-read-playback-state%20"
                    + "user-modify-playback-state%20"
                    + "user-read-currently-playing%20"
                    + "app-remote-control%20"
                    + "streaming%20"
                    + "playlist-modify-public%20"
                    + "playlist-modify-private%20"
                    + "playlist-read-private%20"
                    + "playlist-read-collaborative%20"
                    + "user-library-modify%20"
                    + "user-library-read%20"
                    + "user-read-email%20"
                    + "user-read-private%20")

    authURL = ("https://accounts.spotify.com/authorize?"
                + "client_id=" + clientID
                + "&response_type=code"
                +"&redirect_uri=" + redirectURI
                + "&scope=" + permissions)

    return redirect(authURL, code=302)

@app.route('/callback')
def callback():
    code = request.args.get("code")

    # Show error if code is not given by spotify's auth server
    if code is None: return "Failed to communicate with spotify auth server"

    tokens = initialAuth(code)
    return "Authed: " + str(tokens)


def initialAuth(code):
    url = 'https://accounts.spotify.com/api/token'

    params = {"grant_type":"authorization_code",
            "code":code,
            "redirect_uri":"http://localhost:1025/callback",
            "client_id":clientID,
            "client_secret":clientSecret}

    r = requests.post(url, data=params).json()

    transmitAuthInformation(r["access_token"], r["refresh_token"])

    return r

# TODO make this work
def transmitAuthInformation(accessToken, refreshToken):
    s = socket.socket()
    s.connect(('0.0.0.0',1026))

    data = (accessToken + " " + refreshToken)

    s.send(data.encode())

    s.close()



    


# ====================================================== #
#                      Initial Setup                     #
# ====================================================== #

ACCESS_TOKEN = ""
REFRESH_TOKEN = ""

# Gatherd from configuration.conf:
clientID = ""
clientSecret = ""
redirectURI = ""
transitPort = ""
authPagePort = ""

with open("configuration.conf") as confFile:
    lines = confFile.readlines()
    count = 0
    
    stripComments = lambda s : s.split("#")[0].strip()

    for line in lines:
        if "clientID" in line:
            clientID = stripComments(line).replace("clientID=", "")
        elif "clientSecret" in line:
            clientSecret = stripComments(line).replace("clientSecret=", "")
        elif "redirectURI" in line:
            redirectURI = stripComments(line).replace("redirectURI=", "")
        elif "transitPort" in line:
            transitPort = stripComments(line).replace("transitPort=", "")

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("ERROR: correct usage python3 auth.py <port number>")
        exit(1)

    authPagePort = int(sys.argv[1])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', authPagePort))
    port = sock.getsockname()[1]
    sock.close()
    app.run(port=port)