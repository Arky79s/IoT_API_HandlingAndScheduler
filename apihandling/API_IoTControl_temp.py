
import os
import requests


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


headers={
    "acsToken":"D88C8E35F17F54B64DE54294511D9EB9C7AD2EB2404A1802CC90A6C70C7F6872", 
    "irId":"ebaa45515fc010f02crcly",
    "remoteId":"eb0e62e2f8da24a3dcki0w"
}
payload={
    "key" : "PowerOff"#"key" : "PowerOff"
}
body={}
baseUrl="https://www.gocone.co.kr:5845"

url=f"{baseUrl}/gwapi/ir/tp/cmd"

response = requests.post(url,headers=headers, json=payload)

print(response)


if response.status_code == 200:
    data = response.json()
    print(f"성공 200 {data["success"]}")

# else:#실패시 토큰 새로고침 

#     print("실패")
    
#     refresher = TokenRefresher()
#     acs_token, ref_data =refresher.refresh_token()
    
#     if acs_token is not None and ref_data is not None:
#         os.environ["acsToken"]=acs_token
#         os.environ["resToken"]=ref_data
#         headers["access_token"]=acs_token
#         response = requests.post(url, headers=headers,body=body)
    

#{{url}}/gwapi/device/info 인 
#{
#    "success": true,
#    "values": {
#        "category": "wnykq",
#        "id": "ebaa45515fc010f02crcly",
#        "ip": "125.141.31.140",
#        "name": "변경할 장치 이름",
#        "online": true,
#        "ownerHomeId": "261684386",
#        "sub": false,
#        "time_zone": "+09:00",
#        "status": [
#            {
#                "code": "va_temperature",
#                "value": "208"
#            },
#            {
#                "code": "va_humidity",
#                "value": "57"
#            }
#        ]
#    }
#}



#디바이스 ID ir  ID
#{{url}}/gwapi/ir/info
#"category_name": "Air Conditioner"
#"category_id": "5"

#스마트기능#{{url}}/gwapi/smartfn/info

#홈목록 조회  > {{url}}/gwapi/home/room-list 인:  acsToken,uid 아웃데이터: #az1755843211193wXUkA
#아웃
#{
#    "success": true,
#    "values": {
#        "rooms": [
#            {
#                "room_id": 147095020,
#                "name": "거실"
#            },
#            {
#                "room_id": 147095021,
#                "name": "안방"
#            },
#            {
#                "room_id": 147095022,
#                "name": "작은 방"
#            },
#            {
#                "room_id": 147095023,
#                "name": "주방"
#            },
#            {
#                "room_id": 147095024,
#                "name": "주방"
#            },
#            {
#                "room_id": 147095025,
#                "name": "서재"
#            }
#        ],
#        "name": "사무실 ",
#        "home_id": 262426652,
#        "lon": 126.89,
#        "lat": 37.48,
#        "geo_name": "가산동 582-4"
#    }
#}



#}

#방목록 조회 #{{url}}/gwapi/home/room-list
#방장치 조회 #{{url}}/gwapi/home/room/device-list

#IR리모컨 브랜드 조회#{{url}}/gwapi/ir/brands > 인데이터 acsToken irid categoryID 아웃 데이터> 브랜드 브랜드ID #

        # {
        #     "brand_name": "LG",
        #     "brand_id": "32"
        # },
#IR리모컨 브랜드 실행 #포스트<headers,body 필요 >#{{url}}/gwapi/ir/tp/cmd > 인데이터 헤더 acsToken, irid , remoteId 
#  #eb0e62e2f8da24a3dcki0w #바디 "key":"PowerOff", key":"PowerOff"



#게이트하위장치조회 {{url}}/gwapi/gw/sub  인 데이터: acsToken, deviceId

#{
#     "success": true,
#     "values": [
#         {
#             "active_time": 1756863074,
#             "update_time": 1756863074,
#             "owner_id": "261684386",
#             "product_id": "qzktzhehinzsz2je",
#             "icon": "smart/icon/001453365846342fhj9e/11c62df7bd89c10f43d3e5ee8d13b4f4.png",
#             "name": "에어컨",
#             "online": true,
#             "id": "eb0e62e2f8da24a3dcki0w",
#             "category": "infrared_ac",
#             "node_id": "6a6c7eca691e5b8f"
#         }
#     ]
# }