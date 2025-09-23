import os
import requests
from dotenv import load_dotenv


    #웹서비스 부터 필요함 API를 구축 post맨  #원에이지 펑션 
    #설계 에러 코드 
    #펑션
    #에러코드 작성해야하고 이를 통해 토큰 새로고침통한 로직으로 가야함 
    #제어코드는 마지막 요청자에 따른 코드 처리 
    #  


class TokenRefresher:
# .env 파일에서 환경변수 불러오기

    def __init__(self):
        #load_dotenv()
        self.base_url = os.getenv('base_url', 'https://www.gocone.co.kr:5845')
        self.ref_token = os.getenv('refToken')
        self.url = f"{self.base_url}/gwapi/token/ref-tokens"
        self.headers = {
            'refToken': self.ref_token
        }

    def refresh_token(self):
        response = requests.get(self.url, headers=self.headers)
        print(response)
        if response.status_code == 200:
            print("✅ 성공:")
            data = response.json()
            acs_token = data.get('access_token')
            ref_token = data.get('refresh_token')
            print(acs_token, ref_token)
            return acs_token, ref_token
        else:
            print("❌ 실패:")
            print(response.status_code)
            print(response.text)
            return None, None

if __name__ == "__main__":
    refresher = TokenRefresher()
    acs_token, ref_token=refresher.refresh_token()
    os.environ['acsToken']=acs_token
    os.environ['refToken']=ref_token
