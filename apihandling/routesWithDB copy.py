from flask import Flask,render_template,url_for,request,jsonify
from API_Make_Token  import TokenIssuer
from API_Refrash import TokenRefresher
import os
import requests


from datetime import datetime, date, timedelta
import psycopg2
import pandas as pd
from src.Service import  

from dotenv import load_dotenv
from src.control import setRemoteControlFunc

from psycopg2.extras import RealDictCursor

import json

# Flask 객체 선언
app = Flask(__name__)

# DB 연결 함수
def get_db_connection():
    return psycopg2.connect(
        host = "localhost",
        database = "connecterDB",
        user = "postgres",
        password = "0930"
    )


# 기본 주소가 호출된 경우 실행
@app.route("/")
def index_func():
    load_dotenv()
    dataToken = TokenIssuer()
    acs1,ref1 = dataToken.issue_token()
    
    
    baseUrl = os.getenv('base_url')

    url = f"{baseUrl}/gwapi/ir/status"

    os.environ['acsToken'] = acs1
    os.environ['refToken'] = ref1

    irId1 = os.getenv("irId")
    remoteId1 = os.getenv("remoteId")

    tempCheckHeaders = {
        "acsToken" : acs1, 
        "irId" : irId1, #S06Pro 
        "remoteId" : remoteId1 #에어컨 
    } 


    resultTemp = requests.get(url,headers = tempCheckHeaders)
    resultTempData = resultTemp.json()

    getValueData = resultTempData.get("values")
    print(getValueData)
    rtnTemp = getValueData['temp']
    return render_template("index.html", title="Home")


@app.route("/tempControl", methods=["GET","POST"])
def tempControl_func():

    service 
        results = {
            "tempData" : tempData
        }


    return render_template("tempControlPage.html", title="tempControl",result=results)



@app.route('/posts', methods = ['POST'])
def insertDB_post():

    results = {}
    tempertureIdInput = request.form['TempertureInput']
    userIdInput = request.form['UserIdInput']
    
    

    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            INSERT INTO recoding_history_table (id,temp_data,created_at,updated_at) 
            VALUES (%s, %s,now(),now()) 
            RETURNING id,tempData, created_at, updated_at
        """, (tempertureIdInput, userIdInput))
        
        post = dict(cursor.fetchone())
        #conn.commit()
        print(post)
        return jsonify(post), 201
    except Exception as e:
        #conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()
        return render_template("tempConrolAfterPage.html", title = "tempControl", result = results)
#db접근 끝나면 커서와 커넥션을 닫아줌

@app.route("/")
def f1_server():
    return "f1_server run"


if __name__== '__main__':
    app.run(debug=True)
