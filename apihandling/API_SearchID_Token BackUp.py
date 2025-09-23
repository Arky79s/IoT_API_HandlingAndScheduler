import os
import requests
from dotenv import load_dotenv

class UserIdSearcher:
    def __init__(self, base_url=None, appid=None, access_token=None):
        load_dotenv()
        self.base_url = base_url or os.getenv('BASE_URL', 'https://www.gocone.co.kr:5845')
        self.appid = appid or os.getenv('appid')
        self.access_token = access_token
        self.url = f"{self.base_url}/gwapi/user/uid"

    def search_uid(self):
        headers = {
            "appid": self.appid,
            "acsToken": self.access_token
        }
        response = requests.get(self.url, headers=headers)
        print(response)
        if response.status_code == 200:
            print("✅ 성공:")
            data = response.json()
            print(data)
            uid = data.get('uid')
            print("uid:", uid)
            return uid
        else:
            print("❌ 실패:")
            print(response.status_code)
            print(response.text)
            return None



class HomeListFetcher:
    def __init__(self, base_url=None, access_token=None, uid=None):
        load_dotenv()
        self.base_url = base_url or os.getenv('BASE_URL', 'https://www.gocone.co.kr:5845')
        self.access_token = access_token
        self.uid = uid
        self.url = f"{self.base_url}/gwapi/home/list"

    def fetch_home_list(self):
        headers = {
            "acsToken": self.access_token,
            "uid": self.uid
        }
        response = requests.get(self.url, headers=headers)
        print(response)
        if response.status_code == 200:
            print("✅ 홈 목록 조회 성공:")
            data = response.json()
            print(data)
            # 홈 목록에서 home_id, name 추출
            home_list = [
                {"home_id": home.get("home_id"), "name": home.get("name")}
                for home in data.get("home_list", [])
            ]
            print("home_list:", home_list)
            return home_list
        else:
            print("❌ 홈 목록 조회 실패:")
            print(response.status_code)
            print(response.text)
            return None

class HomeDeviceListFetcher:
    def __init__(self, base_url=None, access_token=None, uid=None):
        load_dotenv()
        self.base_url = base_url or os.getenv('BASE_URL', 'https://www.gocone.co.kr:5845')
        self.access_token = access_token
        self.uid = uid
        self.url = f"{self.base_url}/gwapi/home/device-list"

    def fetch_home_device_list(self):
        headers = {
            "acsToken": self.access_token,
            "uid": self.uid
        }
        response = requests.get(self.url, headers=headers)
        print(response)
        if response.status_code == 200:
            print("✅ 홈 장치 목록 조회 성공:")
            data = response.json()
            print(data)
            # 홈 장치 목록에서 homeid 추출
            home_ids = [item.get("homeid") for item in data.get("device_list", [])]
            print("home_ids:", home_ids)
            return home_ids
        else:
            print("❌ 홈 장치 목록 조회 실패:")
            print(response.status_code)
            print(response.text)
            return None

# 사용 예시
if __name__ == "__main__":
    # 순서: access_token, uid를 먼저 받아야 함
    #access_token = "여기에_acsToken_값_입력"
    #uid = "여기에_uid_값_입력"
    if uid==None:
        userid=UserIdSearcher(access_token="")
        home_list_fetcher = HomeListFetcher(access_token=access_token, uid=uid)

    #home_list = home_list_fetcher.fetch_home_list()


    if acces_token==None:

    # 4. 홈 목록 조회
    #home_list_fetcher = HomeListFetcher(access_token=access_token, uid=uid)
    #home_list = home_list_fetcher.fetch_home_list()

    # 5. 홈 장치 조회
    #device_list_fetcher = HomeDeviceListFetcher(access_token=access_token, uid=uid)
    #device_list_fetcher.fetch_home_device_list()
    
    # access_token은 토큰 발급 후 받아서 넣어야 합니다.
    #searcher = UserIdSearcher(access_token="여기에_acsToken_값_입력")
    #searcher.search_uid()