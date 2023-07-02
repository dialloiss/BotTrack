import requests

def get_computer(arg):
    url = "http://localhost:3000/api/computer/employeelist/"+arg

    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjczMzBiZWY1LTFmNTktNDg5OS1hNjc2LWI3NTQzODk2ZmYyNSIsImlhdCI6MTY3NDQwODA2OH0.amVPf_Bc7DgIv6s6KrL5FdlDVHYbxnB_sGFydviLObs'
    }

    response = requests.request("GET", url, headers=headers)

    return response