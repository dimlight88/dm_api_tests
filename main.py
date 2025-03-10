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
    "login": "dl9_test",
    "email": "dl9_test@mail.ru",
    "password": "123456789"
}

response = requests.post(
    url=url,
    headers=headers,
    json=json
)

print(response.status_code)
# print(response.json())
