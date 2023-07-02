import requests
import json

def user_login(username,password):
    url = "http://localhost:3000/api/login"

    payload = json.dumps({
    "login": {
        "username": username,
        "password": password
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjczMzBiZWY1LTFmNTktNDg5OS1hNjc2LWI3NTQzODk2ZmYyNSIsImlhdCI6MTY3NDQwODA2OH0.amVPf_Bc7DgIv6s6KrL5FdlDVHYbxnB_sGFydviLObs'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response
