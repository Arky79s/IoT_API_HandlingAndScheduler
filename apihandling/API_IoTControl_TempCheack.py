import os
import requests
from dotenv import load_dotenv
from API_Make_Token import TokenIssuer

class TemperChecker:   
    def __init__(self, base_url=None, access_token=None):
        load_dotenv()
        
        self.base_url = base_url or os.getenv('BASE_URL', 'https://www.gocone.co.kr:5845')
        self.url = f"{self.base_url}/gwapi/user/uid"
    
        

    def TemperCheck(self):

        dataToken = TokenIssuer()
        acs1,ref1 = dataToken.issue_token()
        print(acs1)
        
        baseUrl="https://www.gocone.co.kr:5845"

        url=f"{baseUrl}/gwapi/ir/status"

        tempCheckHeaders = {
            "acsToken" : acs1, 
            "irId" : "ebaa45515fc010f02crcly",
            "remoteId" : "eb0e62e2f8da24a3dcki0w"
        }
        
        resultTemp = requests.get(url,headers=tempCheckHeaders)
        resultTempData=resultTemp.json()

        temp=resultTempData.get("values")
        print(temp)
        return temp

if __name__ == '__main__':
    TempCheck=TemperChecker()
    resData=TempCheck.TemperCheck()
    reseut=resData['temp']
    print(reseut)