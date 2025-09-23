from flask import Flask, render_template, url_for, request
from API_Make_Token import TokenIssuer
from API_Refrash import TokenRefresher
import os
import requests
from dotenv import load_dotenv
#from src.Service  import boundaryService    

from src.control import setRemoteControlFunc

from datetime import datetime
import json

# Flask 객체 선언
app = Flask(__name__)

# 기본 주소가 호출된 경우 실행
@app.route("/")
def index_func():
    load_dotenv()
    dataToken = TokenIssuer()
    acs1,ref1 = dataToken.issue_token()
    
    
    results = {}
    baseUrl = os.getenv('base_url')

    url=f"{baseUrl}/gwapi/ir/status"

    os.environ['acsToken']=acs1
    os.environ['refToken']=ref1

    irId1=os.getenv("irId")
    remoteId1=os.getenv("remoteId")

    tempCheckHeaders = {
        "acsToken" : acs1, 
        "irId" : irId1, #S06Pro 
        "remoteId" : remoteId1 #에어컨 
    } 


    resultTemp = requests.get(url,headers = tempCheckHeaders)
    resultTempData = resultTemp.json()

    getValueData = resultTempData.get("values")
    print(getValueData)
    rtnTemp=getValueData['temp']
    return render_template("index.html", title="Home")


@app.route("/tempControl", methods=["GET","POST"])
def tempControl_func():
    
    results={}
    if request.method == 'POST':
        
        optionData = request.form['modeOption']
        levelInfo = request.form['remoteInfoInput'] #M,H,
            # 파워 컨트롤일 경우 levelInfo가 필요없음
        if optionData in ['PowerOn', 'PowerOff']:
            suseccedFlag = setRemoteControlFunc(optionData, None)
            results["airconInfoData"] = str(optionData)
            return render_template("ｍodeSelectContorlPage backup-1.html", title="ｍodeSelectContorlPage backup-1", result=results)
        try:
            
            temp2intdata=int(levelInfo)
            #resultService = boundaryService()    
                # 제어F  
            # 제어
            
            #범위제어    
            if optionData == "M" : # 모드 0:냉방 1:난방 2,3 없음 4:제습
                contorlMinPoint = os.getenv('airConModeMin')
                contorlMaxPoint = os.getenv('airConModeMax')
                
            elif optionData == 'F': # 풍량 0~ 3  미풍~ 강하게 
                contorlMinPoint = os.getenv('airConFanSpeedMin')
                contorlMaxPoint = os.getenv('airConFanSpeedMax')
                
            elif optionData == 'T': #온도 최소 16 ~ 최대 30
                contorlMinPoint = os.getenv('airConTempMin')
                contorlMaxPoint = os.getenv('airConTempMax')
                
            minpoint=int(contorlMinPoint)
            maxpoint=int(contorlMaxPoint)   
            print(f"Input value: {temp2intdata}, Min: {minpoint}, Max: {maxpoint}, Mode: {optionData}")
      
            if minpoint <= temp2intdata <= maxpoint : #validation
                suseccedFlag = setRemoteControlFunc(optionData, str(temp2intdata))
            else:
                suseccedFlag = False
                print(f"Out of range: Value {temp2intdata} is not between {minpoint} and {maxpoint} for mode {optionData}")    
            #suseccedFlag = setRemoteControlFunc(optionData,temp2intdata)
            #print("suseccedFlag:",suseccedFlag)
            results["airconInfoData"] = f"{optionData}{temp2intdata}"
        except ValueError as e:

            results["error"] = "숫자 형식이 아닙니다"
            print(f"Invalid number format: {levelInfo}")
            

                #if temp2intdata < 18 and temp2intdata >32 : 문법적으로 에러가남

    return render_template("modeSelectContorlPage backup-proto.html", title="modeSelectContorlPage backup-proto", result = results)

if __name__=="__main__":
    app.run(debug=True)
