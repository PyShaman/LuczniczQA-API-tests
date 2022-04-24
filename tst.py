import requests


r = requests.post("http://127.0.0.1:8080/status/", json={"status": "ONLINE"})
print(r.status_code)
print(r.json())
