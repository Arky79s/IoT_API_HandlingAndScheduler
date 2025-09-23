from flask import Flask,render_template,url_for,request
from API_Make_Token  import TokenIssuer
from API_Refrash import TokenRefresher
import os
import requests
from dotenv import load_dotenv
from src.insertDataBase import recoder2DB
from src.insertDataBase import recoder2DataBase


#현재 acsToken, irId, remoteId1 환경변수를 활용한 도중 입력 ,
def setRemoteControlMethod(optionData = None,levelData = None,deviceId = None):
    load_dotenv()
    
    acsToken = os.getenv("acsToken")
    
    baseUrl=os.getenv("base_url", 'https://www.gocone.co.kr:5845')
    #baseUrl= 'https://www.gocone.co.kr:5845'
    print(f"디바이스 아이디: {deviceId} 셋리모트컨트롤메소드 돌입")
    remoteId1_to_osEnv = os.getenv("remoteId")

    
    tempCheckHeaders = {
        "acsToken" : acsToken, 
        "irId" :deviceId,
        "remoteId" : remoteId1_to_osEnv
    }
    
    if optionData in ['PowerOn','PowerOff'] :
        keyValue = optionData

    elif len(optionData) == 1 :
        keyValue = f"{optionData}{levelData}" 
                                  #"key" : "PowerOff"
   
    payload = {
        "key" : keyValue
    }

    print("키벨류"+keyValue )
    print("옵션데이터" +optionData)
    
    url = f"{baseUrl}/gwapi/ir/tp/cmd"
    try:
        response = requests.post(url,headers = tempCheckHeaders, json = payload)
    except Exception as e:
        ref2acs_Token = TokenRefresher()
        acsToken,refToken = ref2acs_Token.refresh_token()
       # 새로운 토큰 환경변수에 저장
        print("토큰 새로고침")
        os.environ["acsToken"] = acsToken
        os.environ["refToken"] = refToken
        tempCheckHeaders={
            "acsToken" : acsToken  ,
            'irId' : deviceId,
            'remoteId' : remoteId1_to_osEnv
        }
        response = requests.post(url,headers = tempCheckHeaders, json = payload)

    print('setRemoteControlFunc 결과:',response)

    print(f"API 요청 - URL: {url}")
    print(f"헤더: {tempCheckHeaders}")
    print(f"페이로드: {payload}")
    print(f"응답 상태: {response.status_code}")
    print(f"응답 내용: {response.text}")  # 전체 응답 내용 확인


    if response.status_code == 200:
        data = response.json()
        print(f"성공 200 {data['success']}")

        succeded=recoder2DataBase(str(deviceId),str(keyValue),data.get('success'))
        print("DB Insert:",succeded)
        
        if data.get("success") is False:
             print(f"API 에러 메시지: {data.get('msg', '알 수 없는 오류')}")
        return False


    return True

def setRemoteControlFunc(optionData = None,levelData = None):
    load_dotenv()
    
    acsToken = os.getenv("acsToken")
    
    baseUrl=os.getenv("base_url", 'https://www.gocone.co.kr:5845')
    #baseUrl= 'https://www.gocone.co.kr:5845'
    
    irId1 = os.getenv("irId")
    remoteId1 = os.getenv("remoteId")


    tempCheckHeaders = {
        "acsToken" : acsToken, 
        "irId" :irId1,
        "remoteId" : remoteId1
    }

    if optionData in ['PowerOn','PowerOff'] :
        keyValue = optionData

    elif len(optionData) == 1 :
        keyValue = f"{optionData}{levelData}" 
                                  #"key" : "PowerOff"
    
 
    payload = {
        "key" : keyValue
    }

    url = f"{baseUrl}/gwapi/ir/tp/cmd"
    try:
        response = requests.post(url,headers = tempCheckHeaders, json = payload)
    except :
        ref2acs_Token = TokenRefresher()
        acsToken,refToken = ref2acs_Token.refresh_token()
       # 새로운 토큰 환경변수에 저장
        print("토큰 새로고침")
        os.environ["acsToken"] = acsToken
        os.environ["refToken"] = refToken
        tempCheckHeaders={
            "acsToken" : acsToken  ,
            'irId' : irId1_to_osEnv,
            'remoteId' : remoteId1_to_osEnv
        }
        response = requests.post(url,headers = tempCheckHeaders, json = payload)

    print('setRemoteControlFunc 결과:',response)

    print(f"API 요청 - URL: {url}")
    print(f"헤더: {tempCheckHeaders}")
    print(f"페이로드: {payload}")
    print(f"응답 상태: {response.status_code}")
    print(f"응답 내용: {response.text}")  # 전체 응답 내용 확인


    if response.status_code == 200:
        data = response.json()
        print(f"성공 200 {data['success']}")

        succeded=recoder2DB(str(keyValue),data.get('success'))
        print("DB Insert:",succeded)
        
        if data.get("success") is False:
             print(f"API 에러 메시지: {data.get('msg', '알 수 없는 오류')}")
        return False


    return succeded