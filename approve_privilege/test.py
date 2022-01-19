import requests
import json

url = "http://127.0.0.1:30001/check"

payload = json.dumps({
  "userName": "lisi01",
  "flag": "aaaa"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
