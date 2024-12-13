import requests

API_URL = "http://127.0.0.1:8000/convert"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTczNDExNDQzNywiaWF0IjoxNzM0MTEwODM3fQ._WTmp38iRHEI_yMoOOjm2BQfNQUanrHBgfOXT-Ie9fk"
headers = {"Authorization": f"Bearer {token}"}
files = {"file": open("testdata/1-001.dcm", "rb")}
data = {"format": "jpeg", "quality": 95}

response = requests.post(API_URL, headers=headers, files=files, data=data)
if response.status_code == 200:
    print("Conversion Successful!")
    print(response.json())
else:
    print("Error:", response.json())
