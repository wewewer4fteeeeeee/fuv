import os
import subprocess
import sys
import random
import time
from flask import Flask, render_template_string, request, jsonify
import requests
from fake_useragent import UserAgent

# Install missing packages if not already installed
required_packages = ["flask", "requests", "fake_useragent"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

app = Flask(__name__)

# Function to spoof browser and IP
class SecurlySpoofer:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()

    def rotate_fingerprint(self):
        """Generate new browser fingerprint"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Ch-Ua': f'"Not.A/Brand";v="8", "Chromium";v="{random.randint(100, 124)}"',
            'X-Forwarded-For': f'{random.randint(100, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}'
        }
        self.session.headers.update(headers)

    def make_request(self, url):
        """Make spoofed request to the URL"""
        self.rotate_fingerprint()
        try:
            response = self.session.get(url)
            return response.text
        except Exception as e:
            print(f"Request failed: {e}")
            return None

# Home route (UI page with HTML inside)
@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Securly Spoofer</title>
    </head>
    <body>
        <h1>Securly Spoofer</h1>

        <form id="spooferForm">
            <label for="url">Enter the URL to spoof:</label>
            <input type="text" id="url" name="url" placeholder="https://pass.securly.com/login" required><br><br>

            <button type="submit">Send Request</button>
        </form>

        <div id="response" style="margin-top: 20px;">
            <h3>Response:</h3>
            <p id="responseMessage"></p>
        </div>

        <script>
            document.getElementById("spooferForm").addEventListener("submit", function(event) {
                event.preventDefault();
                const url = document.getElementById("url").value;
                
                fetch("/make_request", {
                    method: "POST",
                    body: new FormData(document.getElementById("spooferForm")),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        document.getElementById("responseMessage").textContent = "Request successful!";
                    } else {
                        document.getElementById("responseMessage").textContent = "Request failed!";
                    }
                })
                .catch(error => {
                    document.getElementById("responseMessage").textContent = "Error: " + error;
                });
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

# API route to perform spoofed request
@app.route('/make_request', methods=['POST'])
def make_request():
    url = request.form['url']
    spoofer = SecurlySpoofer()
    result = spoofer.make_request(url)
    
    if result:
        return jsonify({"status": "success", "message": "Request successful!", "data": result})
    else:
        return jsonify({"status": "error", "message": "Request failed!"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
