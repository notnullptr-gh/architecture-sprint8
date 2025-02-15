# server.py
import json
from urllib.request import urlopen
from urllib.error import URLError
from authlib.jose.rfc7517.jwk import JsonWebKey
from flask import Flask, request
import os
import jwt
import time


addr = f"{os.environ['FLASK_KEYCLOCK']}/realms/reports-realm"

keycloak_online = False
for i in range(10):
    try:
        jsonurl = urlopen(f"{addr}/protocol/openid-connect/certs")
        keycloak_online = True
    except URLError:
        time.sleep(1)

if not keycloak_online:
    import sys
    sys.exit(1)

keys = JsonWebKey.import_key_set(json.loads(jsonurl.read()))
authorized_roles = [
    'prothetic_user',
]


key = None
if keys.keys:
    key = keys.keys[0].as_pem()


APP = Flask(__name__)


def validate_token(token):
    if key:
        decoded_token = jwt.decode(token, key, algorithms=['HS256', 'RS256'])
        for role in decoded_token['realm_access']['roles']:
            if role in authorized_roles:
                return True
    return False


def get_token(request):
    jwt_token = request.headers.get("Authorization")
    if jwt_token:
        jwt_token = jwt_token.split()[-1]
    return jwt_token


@APP.route("/reports")
def private_scoped():
    token = get_token(request)
    if validate_token(token):
        return "OK", 200
    else:
        return "Unauthorized", 401

APP.run(host="0.0.0.0", port=8000, debug=True)
