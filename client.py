# client.py
import requests

tokenUrl = "http://localhost:8080/realms/myorg/protocol/openid-connect/token"

client_id = "test_api_client"
client_secret = "fsQJIcU3Ze3ymaYSA6cxlHVIw0LDIDeY"
requiredScopes = " ".join(["test_api_access"])

# request the access token from OAuth server
post_body = {"grant_type": "client_credentials",
             "client_id": client_id,
             "client_secret": client_secret,
             "scope": requiredScopes}
headers = {'content-type': "application/x-www-form-urlencoded"}

accessTokenResp = requests.post(tokenUrl,
                    data=post_body,
                    headers=headers)

# derive the access token from OAuth server response
if not accessTokenResp.ok:
    print("server token response status not ok")
    quit()

accessTokenRespJson = accessTokenResp.json()

if not "access_token" in accessTokenRespJson:
    print("access_token not found in token response")
    quit()

accessToken = accessTokenRespJson["access_token"]
print(accessToken)

# request data from resource server with access token in the request header
apiReqHeaders = {
    'content-type': "application/json",
    'authorization': f"Bearer {accessToken}"
}
apiResp = requests.get(
    "http://localhost:5000/api/reports", headers=apiReqHeaders)

# parse the response from resource server
if not apiResp.ok:
    print("ok response not received from resource API call")
    quit()

print("printing API response...")
print(apiResp.json())
print("execution complete!")
