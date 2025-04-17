import os
import requests
import json
from flask import Flask, redirect, request

app = Flask(__name__)

CLIENT_ID = "2232352533827318"
CLIENT_SECRET = "7d702793a8f61436222ca0e7aec437e5"
REDIRECT_URI = "https://fuv-d5cjj.vercel.app/oauth/callback"  # Replace with your Vercel URL

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1361027372119228506/33nbHfh6SFxGKEEt2UKKP5jg5xlHrClqsk6TVFTeNgPd1t1PO_R_KgMP09CHcE2nCj6O"

AUTH_URL = f"https://www.oculus.com/openid/connect/?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=openid"
TOKEN_URL = "https://graph.oculus.com/oauth/token"
USER_INFO_URL = "https://graph.oculus.com/me"

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login')
def login():
    return redirect(AUTH_URL)

@app.route('/oauth/callback')
def callback():
    code = request.args.get('code')
    if code:
        token_data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }

        response = requests.post(TOKEN_URL, data=token_data)
        result = response.json()
        access_token = result.get('access_token')

        if access_token:
            user_info = requests.get(f"{USER_INFO_URL}?access_token={access_token}").json()

            player_id = user_info.get("id", "Unknown ID")
            player_name = user_info.get("name", "Unknown Player")

            send_to_discord(player_id, player_name)

            return "<h1>Login successful! 🎉</h1><p>You can close this window and return to the app.</p>"
        else:
            return "<h1>Token exchange failed.</h1>", 400
    else:
        return "<h1>Missing authorization code.</h1>", 400

def send_to_discord(player_id, player_name):
    discord_message = {
        "content": f"New player tracked!\n**Player ID**: {player_id}\n**Player Name**: {player_name}"
    }

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        data=json.dumps(discord_message),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 204:
        print("[✓] Successfully sent player data to Discord!")
    else:
        print(f"[x] Failed to send to Discord: {response.status_code}")

# Vercel automatically handles app routing, so no need for app.run()
