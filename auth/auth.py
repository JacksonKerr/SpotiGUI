from flask import Flask, redirect, request
import requests
import sys
import os
import base64
import json
app = Flask(__name__)

authURL="""https://accounts.spotify.com/authorize?client_id=16a37ceafc804f8a96c5988a6d460d73&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A1025%2Fcallback&scope=user-read-private%20user-read-email&state=34fFs29kd09"""

@app.route('/')
def main():
    return redirect(authURL, code=302)

@app.route('/callback')
def callback():
    code = request.args.get("code")
    if code is not None:
        state = request.args.get("state")
        print("======== CODE ======== \n" + code + "\n===================")
        getTokens(code)
        return "Authed " + state
    else:
        return "Auth Failed"


def getTokens(code):
    url = 'https://accounts.spotify.com/api/token'

    params = {"grant_type":"authorization_code",
            "code":code,
            "redirect_uri":"http://localhost:1025/callback",
            "client_id":clientID, "client_secret":clientSecret}

    cred = {"client_id":clientID, "client_secret":clientSecret}

    r = requests.post(url, data=params)

    print("=====================")
    print(r.json())
    #print(json.dumps(r.json(), indent=2))
    print("=====================")




clientID = ""
clientSecret = ""

with open("credentials.txt") as credFile:
    lines = credFile.readlines()
    count = 0

    if len(lines) < 2:
        print("ERROR: Credentials not provided in credentials.txt")
        exit(0)
    
    clientID = lines[0].strip()
    clientSecret = lines[1].strip()

print("AUTH: Using client_id = " + clientID)
print("AUTH: Using client_secret = " + clientSecret)

