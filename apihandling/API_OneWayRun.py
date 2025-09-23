from API_Make_Token  import TokenIssuer
import os
import requests

# 1
# 웹서버 붙 

dataToken = TokenIssuer()
acs1,ref2 = dataToken.issue_token()


headers={
    "acsToken" : acs1, 
    "irId" : "ebaa45515fc010f02crcly",
    "remoteId" : "eb0e62e2f8da24a3dcki0w"
}

payload={
    "key" : "PowerOn"#"key" : "PowerOff"
}
body={}
baseUrl="https://www.gocone.co.kr:5845"

url=f"{baseUrl}/gwapi/ir/tp/cmd"

response = requests.post(url,headers=headers, json=payload)

print(response)


if response.status_code == 200:
    data = response.json()
    print(f"성공 200 {data["success"]}")


acs1 
userAppid = dataToken.appid

# 사용 예시

    #
    #유저아이디조회 #{url}}/gwapi/user/devices  #인 데이터 #ascToken,appid, -> 아웃데이터  uid == #az1755843211193wXUkA # 
    #유저소유디바이스 {{url}}/gwapi/user/devices #인데이터 #ascToken,uid -> 아웃데이터 #에어컨ID   eb0e62e2f8da24a3dcki0w
        #에어컨 디바이스ID eb0e62e2f8da24a3dcki0w
        #온습도센서 #ID=ebaa45515fc010f02crcly


            # "category": "infrared_ac",
            # "id": "eb0e62e2f8da24a3dcki0w",
            # "ip": "",
            # "name": "에어컨",
            # "online": true,
            # "ownerHomeId": "261684386",
            # "sub": true,
            # "time_zone": "+09:00",
            # "status": null      

    # entity_id = eb024747dfd463a1ee7fpr ?? 
    # #센서ebaa45515fc010f02crcly #에어컨#eb0e62e2f8da24a3dcki0w 홈 261684386 사무실 홈ID 262426652

#0.acs토큰 발급   # post 방식 
#{{url}}/gwapi/token/issue-tokens # 인데이터 MakeTokenPayload->payload  
# MakeTokenPayload {
# 	"appid" : "Alkedis7@gmail.com",
# 	"password":"soxtuf-diFcuq-cynbu9",
# 	"country_code":"82"
# }

#env 토큰 시스템환경변수 저장 
#아웃풋 ascToken, refToken, expires_in 3881
#시스템 환경변수 담기 

#     appid , ascToken, refToken

#1-1 토큰재발급  인데이터 refToke 통한 아웃풋 
#토큰만료의 경우 실행   

#appid-> uid 
#2.유저 ID 조회 {{url}}/gwapi/user/uid #  ascToken,appid  #아웃풋 uid 
#env 파일 저장  uid 

#2-1.Device 조회  {{url}}/gwapi/user/devices #   ascToken,uid # 아웃풋 category 통한 식별 디바이스 id  #id 
# wnykq 온습도 센서 및 리모컨 제어 ebaa45515fc010f02crcly ,  infrared_ac  적외선 에어컨 리모콘 eb0e62e2f8da24a3dcki0w

#2.1.irId 조회  #{{url}}/gwapi/ir/info #센서 ebaa45515fc010f02crcly #디바이스 ID 활용   eb0e62e2f8da24a3dcki0w


# remoteId -> 적외선리모컨 에어컨 ID    #irId=ebaa45515fc010f02crcly

#3.{{url}}/gwapi/ir/status 인풋데이터 ascToke,irId<센서디바이스ID>,remoteId <리모트조회 remoteId>

#IR 리모컨 카테고리 
#카테고리ID 통한 리모컨 브랜드 조회 5

#{{url}}/gwapi/ir/tp/cmd  #포스트형식  # 리모컨 브랜드 실행  acsTokem ,irId  , remoteId  # 바디 { "key" : "PowerOn"}  #PowerOff 

#<실행시 출력값>
# {
#    "success": true,
#    "run_time": "2025-09-03 16:00:52"}


