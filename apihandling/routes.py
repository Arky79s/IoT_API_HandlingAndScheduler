from flask import Flask,render_template,url_for,request
from API_Make_Token  import TokenIssuer
from API_Refrash import TokenRefresher
import os
import requests
from dotenv import load_dotenv
from src.control import setTempControlFunc
from src.control  import service
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


    resultTemp = requests.get(url,headers=tempCheckHeaders)
    resultTempData = resultTemp.json()

    getValueData = resultTempData.get("values")
    print(getValueData)
    rtnTemp=getValueData['temp']
    return render_template("index.html", title="Home")


@app.route("/tempControl", methods=["GET","POST"])
def tempControl_func():
    results = {} 

    if request.method == 'POST':
        tempData = request.form['TempertureInput']
        optionData = request.form['OptionInput']
        #M,H,F  
        temp2intdata=int(tempData)      
        # 제어
        suseccedFlag = setTempControlFunc(optionData,tempData)  


                                

    # 제어 성공유무 리턴
    print(__name__+suseccedFlag)

    print(tempData)
    results = {
        "tempData" : tempData
    }


    return render_template("airConControlPage.html", title="airConControlPage",result=results)

