# This file is used to perform OAuth2 authorization with SoundCloud to extract an access token.

from flask import Flask, request
import webbrowser
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"

@app.route("/")
def authorize():
    auth_url = (
        f"https://soundcloud.com/connect?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&scope=non-expiring"
    )
    webbrowser.open(auth_url)
    return "Opening SoundCloud authorization page in your browser..."

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code received! Authorization failed."
    token_url = "https://api.soundcloud.com/oauth2/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    resp = requests.post(token_url, data=data)
    token_info = resp.json()
    access_token = token_info.get("access_token")

    if not access_token:
        return f"Failed to get access token: {token_info}"
    return f"Access token received! Copy this token:\n\n{access_token}"

if __name__ == "__main__":
    print("Open http://127.0.0.1:5000 in your browser to start OAuth flow")
    app.run(port=5000)
