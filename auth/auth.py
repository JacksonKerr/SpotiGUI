from flask import Flask, redirect, request
import requests
import sys
import os
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
        getTokens(code)
        return "Authed " + state
    else:
        return "Auth Failed"


def getTokens(code):
    dictToSend = {"grant_type":"authorization_code",
                    "code":code,
                    "redirectURI":"http://localhost:1025/callback"
                    }
    res = requests.post('https://accounts.spotify.com/api/token', json=dictToSend)
    print('response from server:',res.text)
    dictFromServer = res.json()


    url = 'https://somedomain.com'
    body = {"grant_type":"authorization_code",
            "code":code,
            "redirectURI":"http://localhost:1025/callback"}
    headers = {'Authorization': 'Basic '}

    r = requests.post(url, data=json.dumps(body), headers=headers)




clientID = ""
clientSecret = ""

with open("credentials.txt") as credFile:
    lines = credFile.readlines()
    count = 0

    
    if len(lines) < 2:
        print("ERROR: Credentials not provided in credentials.txt")
        exit(0)
    
    for line in lines:
        count += 1
        print("Line{}: {}".format(count, line.strip()))
    
    clientID = lines[0]
    clientSecret = lines[1]

