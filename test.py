import requests
import base64
import os

url = "https://api.imgur.com/3/image"

payload={'image': base64.b64encode(open('image.jpg', 'rb').read())}
files=[

]
# print(str(os.environ['imgur']))
headers = {
  'Authorization': 'Client-ID ' + os.environ['imgur']
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
