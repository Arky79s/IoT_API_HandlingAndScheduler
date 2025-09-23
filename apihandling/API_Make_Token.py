import os
import requests
from dotenv import load_dotenv

class TokenIssuer:
    def __init__(self, base_url=None, appid=None, password=None, country_code="82"):
        #load_dotenv()
        self.base_url = base_url or os.getenv('BASE_URL', 'https://www.gocone.co.kr:5845')
        self.appid = appid or os.getenv('appid')
        self.password = password or os.getenv('password')
        self.country_code = country_code
        self.url = f"{self.base_url}/gwapi/token/issue-tokens"

    def issue_token(self):
        payload = {
            "appid": self.appid,
            "password": self.password,
            "country_code": self.country_code
        }
        response = requests.post(self.url, json=payload)
        print(response)
        if response.status_code == 200:
            print("✅ 성공:")
            data = response.json()
            print(data)
            acs_token = data.get('access_token')
            ref_token = data.get('refresh_token')
            print(acs_token, ref_token)

            #
            os.environ['acsToken']=str(acs_token)
            os.environ['refToken']=str(ref_token)
            
            return acs_token, ref_token
        else:
            print("❌ 실패:")
            print(response.status_code)
            print(response.text)
            return None, None

if __name__ == "__main__":
    issuer = TokenIssuer()
    acs_token, ref_token = issuer.issue_token()
    os.environ['acsToken'] = acs_token
    os.environ['refToken'] = ref_token
    os.environ['appid'] = issuer.appid
