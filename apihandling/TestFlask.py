from flask import Flask
from API_Make_Token  import TokenIssuer
from API_Refrash import TokenRefresher
import os
import requests
from dotenv import load_dotenv

from datetime import datetime
import json




# Flask 객체 선언
app = Flask(__name__)

# class IoTDataParser:
#     def __init__(self):
#         self.required_fields = ['sensor_id', 'value', 'timestamp']
#         self.optional_fields = ['unit', 'location']
    
#     def validate_sensor_data(self, data):
#         """센서 데이터 검증"""
#         errors = []
        
#         # 필수 필드 체크
#         for field in self.required_fields:
#             if field not in data:
#                 errors.append(f"Missing required field: {field}")
        
#         # 데이터 타입 체크
#         if 'value' in data and not isinstance(data['value'], (int, float)):
#             errors.append("Value must be a number")
        
#         # 범위 체크 (온도 센서 예시)
#         if 'value' in data and 'unit' in data:
#             if data['unit'] == '℃' and not (-50 <= data['value'] <= 100):
#                 errors.append("Temperature out of valid range (-50°C to 100°C)")
        
#         return errors
    
#     def parse(self, raw_data):
#         """센서 데이터 파싱"""
#         try:
#             if isinstance(raw_data, str):
#                 data = json.loads(raw_data)
#             else:
#                 data = raw_data
            
#             # 검증
#             errors = self.validate_sensor_data(data)
#             if errors:
#                 return None, errors
            
#             # 파싱된 데이터 반환
#             parsed_data = {
#                 'sensor_id': data['sensor_id'],
#                 'value': float(data['value']),
#                 'timestamp': data.get('timestamp', datetime.now().isoformat()),
#                 'unit': data.get('unit', ''),
#                 'location': data.get('location', 'unknown')
#             }
            
#             return parsed_data, None
            
#         except json.JSONDecodeError:
#             return None, ["Invalid JSON format"]
#         except Exception as e:
#             return None, [f"Parsing error: {str(e)}"]


# 기본 주소가 호출된 경우 실행
@app.route("/")
def index():
    load_dotenv()
    dataToken = TokenIssuer()
    acs1,ref1 = dataToken.issue_token()
    
    
    baseUrl=os.getenv('base_url')

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

    getValueData= resultTempData.get("values")
    print(getValueData)
    rtnTemp=getValueData['temp']
    return f"안녕하세요!오늘 사무실 온도는 섭씨 {str(rtnTemp)} 이군요 "


@app.route("/TempControl/<temper>")
def TempControl(temper):
 


    acsToken = os.getenv("acsToken")

    #ref2acs_Token=TokenRefresher()
    
    baseUrl=os.getenv("base_url")

    url=f"{baseUrl}/gwapi/ir/status"
    irId1=os.getenv("irId")
    remoteId1=os.getenv("remoteId")

    tempCheckHeaders = {
        "acsToken" : acsToken, 
        "irId" :irId1,
        "remoteId" : remoteId１
    }
    
    resultTemp = requests.get(url,headers=tempCheckHeaders)
    
    resultJsonData=resultTemp.json()


    dataValues=resultJsonData.get("values")


    

    payload={
        "key" : f"T{temper}"#"key" : "PowerOff"
    }

    url=f"{baseUrl}/gwapi/ir/tp/cmd"

    response = requests.post(url,headers=tempCheckHeaders, json=payload)

    print(response)


    if response.status_code == 200:
        data = response.json()
        print(f"성공 200 {data["success"]}")


    #acs1 
    #userAppid = dataToken.appid

    return data
if __name__=='__main__':
    app.run(debug=True)


#디렉토리 구조 
"""
https://hhj6212.github.io/tech/programming/2022/01/09/flask1.html
myapp/
    templates/
        base.html
        index.html
        somepage.html
    __init__.py
    routes.py
run_myapp.py
"""

#각 html 별 예시 
"""
# base.html:
<html>
    <head>
        <title>My website</title>
    </head>
    <body>
        <div>
            Go to:
            <a href="{{ url_for('index_func') }}">Home</a>
            <a href="{{ url_for('some_func') }}">Some page</a>
        </div>
        {% block content %}{% endblock %}
    </body>
</html>
"""

#index.html
"""
{% extends "base.html" %}
{% block content %}
<div>
    This is home page. Hello world!"
</div>
{% endblock %}
somepage.html
{% extends "base.html" %}
{% block content %}
<div>
    <p>
        Some page. Nothing created yet.
    </p>
</div>
{% endblock %}
"""

# <routes.py>
"""
from flask import Flask, render_template, url_for
from myapp import app

@app.route("/")
@app.route("/index")
def index_func():
    return render_template("index.html", title="Home")

@app.route("/somepage")
def some_func():
    return render_template("somepage.html", title="SomePage")
"""