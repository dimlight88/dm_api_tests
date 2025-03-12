"""
curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "string",
  "email": "string",
  "password": "string"
}'
"""
import requests

url = 'http://5.63.153.31:5051/v1/account'
headers = {
    'accept': '*/*',
    'Content-Type': 'application/json',
}
json = {
    "login": "dm_qa_001",
    "email": "dm_qa_001@mail.ru",
    "password": "987654321"
}

response = requests.post(
    url=url,
    headers=headers,
    json=json
)

print(response.status_code)
# print(response.json())
