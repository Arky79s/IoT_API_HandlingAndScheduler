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

app=Flask(__name__)


# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 글로벌 상태 관리: dict (device_id: {'last_timestamp': float, 'last_command': str, 'job_id': str})
device_states = {}
# 디바이스별 락 (동시성 보호)
device_locks = {}

#device_last_execution = defaultdict(datetime.now)


command_lock = threading.Lock()

device_queues = defaultdict(Queue)
device_last_execution = defaultdict(datetime.now)

scheduler = BackgroundScheduler(jobstores={'default': MemoryJobStore()})
scheduler.start()

# 명령어 실행 함수
def execute_command(device_id, command):
    option_data=command.split('_')[0]
    level_data=command.split('_')[1]

    """실제 명령어 실행 함수"""
    try:
        success = setRemoteControlFunc(option_data, level_data)
        logger.info(f"Device {device_id} command executed: {option_data} {level_data}, uccess: {success}")
        return success
    except Exception as e:
        logger.error(f"Error executing command for device {device_id}: {str(e)}")
        return False 
    finally:

        print(f"Executing: {device_id} -> {command}")  # 실제 디바이스 호출 로직
            # 실행 후 상태 삭제 (2분 지연 후 삭제 로직은 job에서 처리)
        # 실행 후 상태 삭제
        if device_id in device_locks:
            with command_lock:
                if device_id in device_states:
                    del device_states[device_id]

        return success

# 1분 후 실행 job 스케줄 (debounce용)
def schedule_execution(device_id, command):
    job_id = f"exec_{device_id}"
    # 이전 job 취소
    try:
        #명령어 실행
        scheduler.remove_job(job_id)
    except:
        pass  # job 없으면 무시
    
    # 새 job 추가: 1분 후 실행
    scheduler.add_job(
        execute_command,
        'date',
        run_date=datetime.now() + timedelta(minutes=1),
        id=job_id,
        args=[device_id, command],
        replace_existing=True
    )

# 백그라운드 cleanup: 2분 지난 상태 삭제 (간단히 job 실행 후 삭제로 대체, 또는 별도 interval job)
# 별도 scheduler로 1분마다 cleanup (타임스탬프 2분 지난 id 삭제)
def cleanup_old_states():
    now = datetime.now().timestamp()
    with command_lock:
        to_delete = []
        for device_id, state in device_states.items():
             if now - state['last_timestamp'] > 120:  # 2분
                # job 취소하고 상태 삭제
                try:
                    scheduler.remove_job(state.get('job_id', ''))
                except:
                    pass
                to_delete.append(device_id)
        for d in to_delete:
            del device_states[d]


# Cleanup job 스케줄 (매 1분)
scheduler.add_job(cleanup_old_states, 'interval', minutes=1)




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
                        command=f"{option_data}_{level_data}"
                        success = execute_command(device_id,command)

                        device_last_execution[device_id] = datetime.now()
                        logger.info(f"Executed last command for device {device_id}")
                        break
                    else:
                        logger.info(f"Skipping intermediate command for device {device_id}")

        except Exception as e:
            logger.error(f"Error in process_device_commands for device {device_id}: {str(e)}")
            time.sleep(1)

@app.route('/command', methods=['POST'])
def receive_command():
    data = request.json
    device_id = data.get('device_id')
    command = data.get('command')
    
    if not device_id or not command:
        return jsonify({'error': 'Missing device_id or command'}), 400
    
    now = datetime.now()
    current_timestamp = now.timestamp()
    
    with command_lock:
        if device_id not in device_states:
            # 첫 명령: 즉시 실행
            execute_command(device_id, command)
            # 상태 설정 (but 즉시 실행했으니 불필요, but 다음 위해 타임스탬프만)
            device_states[device_id] = {'last_timestamp': current_timestamp}
            return jsonify({'status': 'executed immediately', 'device_id': device_id})
        
        last_timestamp = device_states[device_id]['last_timestamp']
        time_diff = current_timestamp - last_timestamp
        
        # 상태 업데이트: 마지막 command와 timestamp 갱신
        device_states[device_id]['last_command'] = command
        device_states[device_id]['last_timestamp'] = current_timestamp
        
        if time_diff < 60:  # 1분 미만: debounce (중복 작업 - 이전 타이머 초기화, 마지막만 기억)
            # 경고 메시지
            message = "이 작업은 지연 중입니다. 추가 명령 시 이전 작업이 삭제되고 마지막 작업만 실행됩니다."
            # job 재스케줄 (타이머 초기화)
            schedule_execution(device_id, command)
            return jsonify({'status': 'debounced', 'device_id': device_id, 'message': message})
        else:
            # 1분 이상: 즉시 실행 (but 2분 cleanup과 조합)
            execute_command(device_id, command)
            # 타임스탬프만 업데이트 (command 삭제)
            device_states[device_id] = {'last_timestamp': current_timestamp}
            return jsonify({'status': 'executed immediately', 'device_id': device_id})

def start_device_thread(device_id):
    """디바이스별 처리 스레드 시작"""
    if not hasattr(start_device_thread, 'threads'):
        start_device_thread.threads = {}
    
    if device_id not in start_device_thread.threads:
        thread = threading.Thread(target=process_device_commands, args=(device_id,), daemon=True)
        thread.start()
        start_device_thread.threads[device_id] = thread
        logger.info(f"Started command processing thread for device {device_id}")

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

    return render_template("modeSelectContorlPage backup-multi.html", title=" modeSelectContorlPage backup-multi", result = results)


if __name__=="__main__":
    app.run(debug=True)
