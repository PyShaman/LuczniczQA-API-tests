import requests

url = "http://127.0.0.1:8000/users/me"

payload={'username': 'string',
'password': 'string'}
files=[

]
headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywidXNlcm5hbWUiOiJzdHJpbmciLCJwYXNzd29yZF9oYXNoIjoiJDJiJDEyJEdUaWFuM3UuTzAvV2NZdXdNMENFR09QdXhFckZEVlJ4MFFKVUxCaDVuYmNRM0RrdWJPYmtTIn0.7cX3keZU-F8hDdAuyMuvVAmuwXWBM5Xco1QNz8x4ZU4'
}

response = requests.request("GET", url, headers=headers, data=payload, files=files)

print(response.text)