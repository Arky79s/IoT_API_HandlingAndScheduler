
import os
import requests

acsToken=os.getenv('acsToken')
irId=os.getenv('irId')
remoteId=os.getenv('remoteId')
headers={
    "acsToken" : acsToken, 
    "irId" : irId ,
    "remoteId" : remoteId
}
payload={
    "key" : "T26"
    #"key" : "PowerOff" #M0-M4 모드 #T16~T30  #온도
    #   F0~F3 #송풍 
}
body={}
baseUrl="https://www.gocone.co.kr:5845"

url=f"{baseUrl}/gwapi/ir/tp/cmd"

response = requests.post(url,headers=headers, json=payload)

print(response)


if response.status_code == 200:
    data = response.json()
    print(f"성공 200 {data["success"]}")
