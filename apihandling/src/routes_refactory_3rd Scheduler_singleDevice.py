from flask import Flask, render_template, url_for, request ,jsonify
from API_Make_Token import TokenIssuer
from API_Refrash import TokenRefresher
import os
import requests
from dotenv import load_dotenv
from src.control import setRemoteControlFunc
from datetime import datetime, timedelta
import json
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore


from collections import defaultdict
import time
from queue import Queue
import logging

app = Flask(__name__)


# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory 저장: device_id -> {'last_timestamp': float, 'last_command': str}
device_states = {}
# 디바이스별 락 (동시성 보호)
device_locks = {}


command_lock = threading.Lock()

# APScheduler 초기화
scheduler = BackgroundScheduler(jobstores={'default': MemoryJobStore()})
scheduler.start()

# 명령 실행 함수
def execute_command(device_id, command):
    print(f"Executing: {device_id} -> {command}")  # 실제 디바이스 호출 로직
    
    
    # 실행 후 상태 삭제
    if device_id in device_locks:
        with device_locks[device_id]:
            if device_id in device_states:
                del device_states[device_id]

# 1분 후 실행 job 스케줄 (debounce용)
def schedule_execution(device_id, command):
    # 이전 job 취소
    try:
        scheduler.remove_job(f"exec_{device_id}")
    except:
        pass  # job 없으면 무시
    
    # 새 job 추가: 1분 후 실행
    scheduler.add_job(
        execute_command,
        'date',
        run_date=datetime.now() + timedelta(minutes=1),
        id=f"exec_{device_id}",
        args=[device_id, command],
        replace_existing=True
    )

# 백그라운드 cleanup job: 2분 지난 상태 삭제 (매 1분 실행)
def cleanup_old_states():
    now = datetime.now().timestamp()
    to_delete = []
    for device_id in list(device_states.keys()):
        with device_locks.get(device_id, threading.Lock()):
            last_ts = device_states.get(device_id, {}).get('last_timestamp', 0)
            if now - last_ts > 120:  # 2분 지난 경우 삭제
                to_delete.append(device_id)
    for device_id in to_delete:
        with device_locks.get(device_id, threading.Lock()):
            if device_id in device_states:
                del device_states[device_id]
            if device_id in device_locks:
                del device_locks[device_id]

# Cleanup job 스케줄 (매 1분)
scheduler.add_job(cleanup_old_states, 'interval', minutes=1)



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



@app.route('/command', methods=['POST'])
def receive_command():
    data = request.json
    device_id = data.get('device_id')
    command = data.get('command')
    
    if not device_id or not command:
        return jsonify({'error': 'Missing device_id or command'}), 400
    
    now = datetime.now()
    current_timestamp = now.timestamp()
    
    # 락 확보 (없으면 생성)
    if device_id not in device_locks:
        device_locks[device_id] = threading.Lock()
    with device_locks[device_id]:
        last_timestamp = device_states.get(device_id, {}).get('last_timestamp', 0)
        time_diff = current_timestamp - last_timestamp
        
        # 상태 업데이트
        device_states[device_id] = {
            'last_timestamp': current_timestamp,
            'last_command': command
        }
        
        if time_diff < 60:  # 1분 미만: debounce (경고 메시지 + job 재스케줄)
            schedule_execution(device_id, command)
            message = "Command debounced: If another command arrives within 1 minute, the previous one will be discarded and only the latest will execute after 1 minute."
            return jsonify({'status': 'debounced', 'device_id': device_id, 'message': message})
        else:
            # 1분 이상 간격: 즉시 실행
            execute_command(device_id, command)
            return jsonify({'status': 'executed immediately', 'device_id': device_id})

if __name__ == '__main__':
    app.run(debug=True)