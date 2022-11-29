import requests
import json

ROOT = "http://127.0.0.1:5000/api"



response1 = requests.get(ROOT)
info = response1.json()
print(info)

jsond={"RFID":info["tag"]["RFID"],"gutterNetWeight":info["scale"]}
object_j = json.dumps(jsond)
print(object_j)

input()

response2 = requests.put(ROOT+ "/initGutter", data=object_j, headers={"content-type":"application/json"})
print(response2.json())

input()

response1 = requests.get(ROOT)
info = response1.json()
print(info)