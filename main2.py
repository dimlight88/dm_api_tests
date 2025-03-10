"""
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/1aa0f4ed-39fe-4e88-90b1-924fa1ecd896' \
  -H 'accept: text/plain'
"""
import pprint
import requests

# url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json',
# }
# json = {
#     "login": "dl9_test",
#     "email": "dl9_test@mail.ru",
#     "password": "123456789"
# }
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )

url = 'http://5.63.153.31:5051/v1/account/1aa0f4ed-39fe-4e88-90b1-924fa1ecd896'
headers = {
    'accept': 'text/plain'
}

response = requests.put(
    url=url,
    headers=headers
)

print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])