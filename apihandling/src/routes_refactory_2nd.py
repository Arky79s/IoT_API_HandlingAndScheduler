from flask import Flask, render_template, url_for, request
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
from collections import defaultdict
import time
from queue import Queue
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 디바이스별 명령어 큐와 타임스탬프 저장
device_queues = defaultdict(Queue)
device_last_execution = defaultdict(datetime.now)
command_lock = threading.Lock()

scheduler = BackgroundScheduler()
scheduler.start()

# 명령어 실행 함수
def execute_command(device_id, option_data, level_data):
    """실제 명령어 실행 함수"""
    try:
        success = setRemoteControlFunc(option_data, level_data)
        logger.info(f"Device {device_id} command executed: {option_data} {level_data}, Success: {success}")
        return success
    except Exception as e:
        logger.error(f"Error executing command for device {device_id}: {str(e)}")
        return False

def process_device_commands(device_id):
    """디바이스별 명령어 처리 스레드 함수"""
    while True:
        try:
            with command_lock:
                if device_queues[device_id].empty():
                    continue

                current_time = datetime.now()
                last_execution = device_last_execution[device_id]
                time_diff = (current_time - last_execution).total_seconds()

                if time_diff < 120:  # 2분(120초) 대기
                    time.sleep(1)
                    continue

                # 대기열의 마지막 명령만 실행
                while not device_queues[device_id].empty():
                    option_data, level_data = device_queues[device_id].get()
                    if device_queues[device_id].empty():  # 마지막 명령인 경우
                        success = execute_command(device_id, option_data, level_data)
                        device_last_execution[device_id] = datetime.now()
                        logger.info(f"Executed last command for device {device_id}")
                        break
                    else:
                        logger.info(f"Skipping intermediate command for device {device_id}")

        except Exception as e:
            logger.error(f"Error in process_device_commands for device {device_id}: {str(e)}")
            time.sleep(1)

def start_device_thread(device_id):
    """디바이스별 처리 스레드 시작"""
    if not hasattr(start_device_thread, 'threads'):
        start_device_thread.threads = {}
    
    if device_id not in start_device_thread.threads:
        thread = threading.Thread(target=process_device_commands, args=(device_id,), daemon=True)
        thread.start()
        start_device_thread.threads[device_id] = thread
        logger.info(f"Started command processing thread for device {device_id}")

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
    results = {}
    if request.method == 'POST':
        try:
            optionData = request.form['modeOption']
            levelInfo = request.form['remoteInfoInput']
            selected_devices = request.form.getlist('selectedDevices')  # 선택된 디바이스 목록

            if not selected_devices:
                results["error"] = "디바이스를 선택해주세요."
                return render_template("modeSelectContorlPage backup-proto.html", title="Control Page", result=results)

            # 파워 컨트롤 처리
            if optionData in ['PowerOn', 'PowerOff']:
                for device_id in selected_devices:
                    # 디바이스 스레드 시작
                    start_device_thread(device_id)
                    # 명령어 큐에 추가
                    device_queues[device_id].put((optionData, None))
                    logger.info(f"Queued power command for device {device_id}: {optionData}")
                
                results["airconInfoData"] = f"Power command queued for {len(selected_devices)} devices"
                return render_template("modeSelectContorlPage backup-proto.html", title="Control Page", result=results)

            # 다른 명령어 처리
            try:
                temp2intdata = int(levelInfo)
                
                # 범위 제어
                if optionData == "M":  # 모드 0:냉방 1:난방 2,3 없음 4:제습
                    contorlMinPoint = int(os.getenv('airConModeMin'))
                    contorlMaxPoint = int(os.getenv('airConModeMax'))
                elif optionData == 'F':  # 풍량 0~ 3
                    contorlMinPoint = int(os.getenv('airConFanSpeedMin'))
                    contorlMaxPoint = int(os.getenv('airConFanSpeedMax'))
                elif optionData == 'T':  # 온도 제어
                    contorlMinPoint = int(os.getenv('airConTempMin'))
                    contorlMaxPoint = int(os.getenv('airConTempMax'))
                
                # 입력값 검증
                if contorlMinPoint <= temp2intdata <= contorlMaxPoint:
                    # 각 선택된 디바이스에 대해 명령어 큐에 추가
                    for device_id in selected_devices:
                        start_device_thread(device_id)
                        device_queues[device_id].put((optionData, str(temp2intdata)))
                        logger.info(f"Queued command for device {device_id}: {optionData} {temp2intdata}")
                    
                    results["airconInfoData"] = f"Command {optionData}{temp2intdata} queued for {len(selected_devices)} devices"
                else:
                    results["error"] = f"입력값이 범위를 벗어났습니다 ({contorlMinPoint}~{contorlMaxPoint})"
                    logger.warning(f"Value out of range: {temp2intdata} for mode {optionData}")
            
            except ValueError as e:
                results["error"] = "숫자 형식이 아닙니다"
                logger.error(f"Invalid number format: {levelInfo}")

        except Exception as e:
            results["error"] = "처리 중 오류가 발생했습니다"
            logger.error(f"Error processing request: {str(e)}")

    return render_template("modeSelectContorlPage backup-proto.html", title="modeSelectContorlPage backup-proto", result = results)

if __name__=="__main__":
    app.run(debug=True)
