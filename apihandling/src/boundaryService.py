from flask import Flask,render_template,url_for,request
from API_Make_Token  import TokenIssuer
from API_Refrash import TokenRefresher
import os
import requests
from dotenv import load_dotenv
from src.control import setRemoteControlFunc

from datetime import datetime
import json



if request.method == 'POST':
    tempData = request.form['TempertureInput']
    optionData = request.form['levelInfoInput'] #M,H,F  
    temp2intdata=int(tempData)
    # 제어
        
    if optionData == "M" : # 모드 0:냉방 1:난방 2,3 없음 4:제습
        contorlMinPoint=int(os.getenv('airConModeMin'))
        contorlMaxPoint=int(os.getenv('airConModeMax'))
        
    elif optionData == 'F': # 풍량 0~ 4  미풍~ 강하게 
        contorlMinPoint=int(os.getenv('airConFanSpeedMin'))
        contorlMaxPoint=int(os.getenv('airConFanSpeedMax'))
        
    elif optionData == 'T': #온도 최소 16 ~ 최대 30
        contorlMinPoint=int(os.getenv('airConTempMin'))
        contorlMaxPoint=int(os.getenv('airConTempMax'))


    #if temp2intdata < 18 and temp2intdata >32 : 문법적으로 에러가남
    if contorlMinPoint <= temp2intdata <= contorlMaxPoint : #validation
        suseccedFlag = setRemoteControlFunc(optionData,tempData)
    else:
        suseccedFlag= False
        print("Out of range")

