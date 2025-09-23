import os
import requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv

class BaseApiFetcher(ABC):
    def __init__(self, base_url=None):
        load_dotenv()
        self.base_url = base_url or os.getenv('BASE_URL', 'https://www.gocone.co.kr:5845')

    @abstractmethod
    def fetch(self, *args, **kwargs):
        pass

class UserIdSearcher(BaseApiFetcher):
    def __init__(self, access_token=None, appid=None,  base_url=None):
        super().__init__(base_url)
        self.appid = appid or os.getenv('appid')
        self.access_token = access_token
        self.url = f"{self.base_url}/gwapi/user/uid"

    def fetch(self):
        headers = {
            "acsToken": self.access_token,
            "appid": self.appid            
        }
        response = requests.get(self.url, headers=headers)
        print(response)
        if response.status_code == 200:
            data = response.json()
            uid = data.get('uid')
            print("uid:", uid)
            return uid
        else:
            print("❌ 실패:", response.status_code, response.text)
            return None

class UserDeviceInfoSearcher(BaseApiFetcher):
    
    def __init__(self, access_token=None, uid=None, base_url=None):
        super().__init__(base_url)
        self.access_token = access_token
        self.uid = uid
        self.url = f"{self.base_url}/gwapi/user/devices"

    def fetch(self):
        headers = {
            "acsToken": self.access_token,
            "uId": self.uid
        }
        response = requests.get(self.url, headers=headers)
        print(response)
        if response.status_code == 200:
            data = response.json()
            home_ids = [item.get("id") for item in data.get("devices", [])]
            print("home_ids:", home_ids)
            return home_ids
        else:
            print("❌ 홈 장치 목록 조회 실패:", response.status_code, response.text)
            return None


class DeviceInfoListSearcher(BaseApiFetcher):
    
    def __init__(self, access_token=None, uid=None, base_url=None):
        super().__init__(base_url)
        self.access_token = access_token
        self.uid = uid
        self.url = f"{self.base_url}/gwapi/user/devices"

    def fetch(self):
        headers = {
            "acsToken": self.access_token,
            "uId": self.uid
        }
        response = requests.get(self.url, headers=headers)
        print(response)
        if response.status_code == 200:
            data = response.json()
            home_ids = [item.get("id") for item in data.get("devices", [])]
            print("home_ids:", home_ids)
            device_infos =[infos.get("status") for infos in data.get("devices", [])][0]

            print("device_infos:", device_infos)
            
            return home_ids,device_infos
        else:
            print("❌ 홈 장치 목록 조회 실패:", response.status_code, response.text)
            return None,None



# 사용 예시
if __name__ == "__main__":

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
        



    # entity_id = eb024747dfd463a1ee7fpr ?? #센서ebaa45515fc010f02crcly #에어컨#eb0e62e2f8da24a3dcki0w 홈 261684386 사무실 262426652

    # 1. access_token을 먼저 발급받아야 함 (여기선 직접 입력)
    try:
        access_token =os.getenv("")



    # 2. uid 조회
    user_searcher = UserIdSearcher(access_token=access_token)
    uid = user_searcher.fetch()
    #2.5 homeID


    #3.deviceID
    user_divces=DeviceInfoListSearcher(access_token=access_token,uid=uid)
    result_Devicelist=[]
    result_DeviceInfolist=[]
    result_Devicelist,result_DeviceInfolist=user_divces.fetch()

    #4.remoteID


    #5.roomId 

    #6.irid






['values']['category']['functions']['code']
['values']['category']['functions']['type'] 
['values']['category']['functions']['vals']

#장치세부 속성 조회 #{{url}}/gwapi/device/properties  인 데이터 :acsTotken,deviceID, codes
#{
#    "success": true,
#    "properties": [
#        {
#            "code": "temp_current",
#            "value": 247,
#            "time": "2025년09월02일 16시32분31초",
#            "timestamp": "1756798351316"
#        },
#        {
#            "code": "humidity_value",
#            "value": 59,
#            "time": "2025년09월02일 16시32분31초",
#            "timestamp": "1756798351396"
#        },
#        {
#            "code": "ir_send",
#            "value": "",
#            "time": "2025년06월10일 18시13분01초",
#            "timestamp": "1749546781955"
#        },
#        {
#            "code": "ir_study_code",
#            "value": null,
#            "time": "2025년08월28일 13시49분16초",
#            "timestamp": "1756356556297"
#        }
#    ]
#}

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

#조회 # 리모컨 브랜드실행 
#{{url}}/gwapi/ir/tp/cmd
#{
#	"name":"add_smartfn",
#    "background":"",
#    "actions":[
#        {
#            "action_executor": "",
#            "entity_id": "eb024747dfd463a1ee7fpr",
#            "executor_property": {  
#                "switch_1" : "false"
#            }
#        }
#    ]
#} 
#{{url}}/gwapi/home/room-list 인:  acsToken homeId
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



#스마트기능 추가 Post {{url}}/gwapi/smartfn/add

#{# 인 body 
#	"name":"add_smartfn",
#    "background":"",
#    "actions":[
#        {
#            "action_executor": "",
#            "entity_id": "eb024747dfd463a1ee7fpr",
#            "executor_property": {  
#                "switch_1" : "false"
#            }
#        }
#    ]
#}
#{#아웃 body

#}

#방목록 조회 #{{url}}/gwapi/home/room-list
#방장치 조회 #{{url}}/gwapi/home/room/device-list




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