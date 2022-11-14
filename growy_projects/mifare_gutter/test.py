import requests

ROOT = "http://127.0.0.1:5000/api"

response = requests.put(ROOT+ "/initGutter", data='{"RFID":"04:21:47:2A:44:70:80","gutterNetWeight":"2874"}', headers={"content-type":"application/json"})
print(response.json())