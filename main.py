import os
import discord
from discord.ext import commands
from flask import Flask, request
import requests

# Initialize Flask app
app = Flask(__name__)

# Environment Variables (make sure you set them on Vercel)
DISCORD_TOKEN = os.getenv("MTM2MTAzMzIxNTk2MzMwMzk5Ng.GrXy6B.n9ID_tOjlq6Qoa6TeHpFyaBdLwvFXuBgYWHYN0")
WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1361027372119228506/33nbHfh6SFxGKEEt2UKKP5jg5xlHrClqsk6TVFTeNgPd1t1PO_R_KgMP09CHcE2nCj6O")
TARGET_BASE = os.getenv("https://bigscaryapi.azurewebsites.net/api/BigScaryAPI?code=YH0YeQFzdUmr8ErexjqWTIiYk6_J_wb3fAv8s15BtV2VAzFuglPGJQ==")

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Define Flask route for home
@app.route('/')
def home():
    return "Flask is running on Vercel!"

# Define Flask route for linking accounts
@app.route('/link', methods=['POST'])
def link_account():
    discord_user_id = request.form.get('discord_user_id')
    username = request.form.get('username')
    
    if discord_user_id and username:
        # Send confirmation to webhook
        data = {
            "content": f"Account linked: {username}, Discord ID: {discord_user_id}"
        }
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 200:
            return "Account linked successfully!"
        else:
            return "Failed to link account!", 500
    return "Missing parameters!", 400

# Define Flask route for granting items
@app.route('/give', methods=['POST'])
def give_item():
    discord_user_id = request.form.get('discord_user_id')
    currency = request.form.get('currency')

    if discord_user_id and currency:
        # Send request to backend API to process the item grant
        backend_url = f"{TARGET_BASE}/api/grant_item"
        payload = {
            "discord_user_id": discord_user_id,
            "currency": currency
        }
        response = requests.post(backend_url, json=payload)
        
        if response.status_code == 200:
            data = {
                "content": f"User with ID {discord_user_id} received {currency}!"
            }
            requests.post(WEBHOOK_URL, json=data)
            return "Item granted successfully!"
        else:
            return "Failed to grant item!", 500
    return "Missing parameters!", 400

# Start Flask app for local development (not needed on Vercel)
if __name__ == "__main__":
    app.run(debug=True)
