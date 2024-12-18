import json
import requests


url="http://127.0.0.1:8000/addReview"
data={"id_user":2, "text":"rrgergre"}
r=requests.post(url, data=json.dumps(data))
print(r.text)