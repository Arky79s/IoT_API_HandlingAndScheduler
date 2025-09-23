from flask import Flask, render_template, url_for, request ,jsonify
from API_Make_Token import TokenIssuer
from API_Refrash import TokenRefresher
import os
import requests
from dotenv import load_dotenv
from src.control import setRemoteControlMethod
from datetime import datetime, timedelta

import threading
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore


from collections import defaultdict
import time
from queue import Queue
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#멀티 디바이스 변수 선택-> 전체 타이머 init 일괄실행 이후 타이머 부여 ? 
#개별 디바이스 선택시 _> 개별 디바이스 선택이후 이전타이머가 2분일경우 실행후 삭제 
#타이머는 1분 마다 클린업 실행 3분 초과 타이머의 경우 삭제
# 
# 실행조건 타이머가 2분이 되었거나 디바이스 상태에 아이디가 등록 안된경우 
# 
# 문제점 송풍 온도를 통해 변경 하는경우 휴대폰에서 입력의 경우 값을 + - 로 일괄적용 하기 떄문에 문제가 있음 

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory 저장: device_id -> {'last_timestamp': float, 'last_command': str}
device_states = {}
# 전역 락 (동시성 보호)
global_lock = threading.Lock()

# APScheduler 초기화
scheduler = BackgroundScheduler( job_defaults={'coalesce': True, 'max_instances': 3},jobstores={'default': MemoryJobStore()},
    daemon=True)
scheduler.start()

# 명령   실행 함수
def execute_command(device_id, command):
    try:

        logger.info(f"Executing command for device {device_id}: {command}")
        success = setRemoteControlMethod(command.split('_')[0], command.split('_')[1] if '_' in command else None,device_id)
        
        # 데이터베이스에 이력 저장
        execution_time = datetime.now()
        db_record = {
            'device_id': device_id,
            'command': command,
            'execution_time': execution_time,
            'success': success,
            'execution_type': 'immediate' if device_id not in device_states else 'delayed'
        }

         #커맨드에서_릴기준으로 가져온 
        optionData = command.split("_")[0]
        temp_data  =str(command.split("_")[1]) if '_' in command else ''

        print(f'spliter Underbar : option = {optionData},temperature = {temp_data}')

        # TODO: 데이터베이스 저장 로직 구현
        logger.info(f"Command execution recorded: {db_record}")

        #  상태 초기화
        with global_lock:
            if device_id in device_states: #기기 식별 ID 가 있으면  삭제 
                device_states[device_id]['status'] = 'executed'
                device_states[device_id]['executed_at'] = datetime.now().timestamp()
                logger.info(f"Device {device_id} marked as executed")
        
    except Exception as e:
        logger.error(f"Error executing command for device {device_id}: {str(e)}")
        raise

#2분 후 실행 job 스케줄 (debounce용)
def schedule_execution(device_id, command):
    # 이전 job 취소
    job_id=f"exec_{device_id}"
    try:
        scheduler.remove_job(job_id)
        print("디바이스:"+device_id+"매개 커맨드"+command+"잡아이디:"+job_id)
   
        now_ts = datetime.now().timestamp()    
        # 새 job 추가: 2분 후 실행
        
        run_at = datetime.now() + timedelta(minutes=2)

        scheduler.add_job(
            func = execute_command,
            trigger ='date',
            run_date = run_at,
            id=job_id,
            args=[device_id, command],
            replace_existing=True
        )
        logger.info(f"Scheduled exec for device {device_id} in 2 minutes, job_id={job_id}")
    except Exception as e :
        logger.debug(f"No existing job to remove: {job_id}, {e}")
    device_states[device_id] = {
    'last_timestamp': now_ts,
    'last_command': command,
    'status': 'pending',
    'job_id': job_id
}
    return  job_id

#
def cleanup_old_states():
    now = datetime.now().timestamp()
    print("cleanup_old_states: 시동")
    with global_lock:        
        to_delete = []
        for device_id, state in list(device_states.items()):
                last_ts =state.get('last_timestamp',0)
                if state.get('status') == 'executed' and now - last_ts > 180:
                # job 취소하고 상태 삭제
                    job_id=state.get('job_id')
                    #job_id="exec_"+device_id
                    try:
                        scheduler.remove_job(job_id)
                        print("잡아이디에 따른 스케줄 삭제",job_id)
                    except:
                        pass
                    del device_states[device_id]
                    print("잡 상태리스트 지정삭제 ",device_id)
                    logger.info(f"Cleaned up device: {device_id}")

                    logger.info(f"cleanup_old_states 완료, duration: {time.time() - start:.2f} sec")

        for device_id in to_delete:
            del device_states[device_id]
            logger.info(f"Cleaned up expired state for device {device_id}")

     # Cleanup job 스케줄 (매 2분)
scheduler.add_job(cleanup_old_states, 'interval', minutes=3, id='cleanup_job', replace_existing=True)



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
    return render_template("index.html", title="Home",result=getValueData)



@app.route('/command', methods=['GET', 'POST'])
def receive_command():
    
    if request.method == 'GET':
        return render_template('command_main.html', title="Command Control")

@app.route('/command/<action>', methods=['GET', 'POST'])
def command_with_action(action):
    if request.method == 'GET':
        
        return render_template(f'command_{action}.html', title=f"Command {action}")
    if request.method == 'POST':
        try:
            # POST 처리
            is_api_request = request.is_json
            
            if is_api_request:
                data = request.json
                device_id = data.get('device_id')
                command = data.get('command')
            else:
                device_id = request.form.get('device_id')
                command = f"{action}_{request.form.get('value')}" if request.form.get('value') else action
            
            now = datetime.now()
            current_ts = now.timestamp()
            
            print("1차 Comand data:",device_id,command)#: device1 temperature_27
            if len( command.split("_")[0]) > 2 : 
                optionData = command.split("_")[0][0].upper()
                levelData = command.split("_")[1]
                command = optionData+"_"+levelData
            else :
                command = optionData 
            print("2차 Comand data:",device_id,command)#: device1 temperature_27
            
            if not device_id or not command:
                logger.warning(f"Invalid request: Missing device_id or command")
                
                return jsonify({'error': 'Missing device_id or command'}), 400

            now = datetime.now()
            current_timestamp = now.timestamp()
            
            # 새로운 디바이스 체크
            is_new_device = device_id not in device_states and device_id 
            
               
            with global_lock:
                
                if is_new_device:
                    # 새 디바이스의 첫 명령은 즉시 실행
                    logger.info(f"New device {device_id}: Executing first command immediately")
                    success = execute_command(device_id, command)
                    
                    device_states[device_id] = {
                        'last_timestamp': current_timestamp,
                        'last_command': command,
                        'status': 'initialized',
                        'first_seen': current_timestamp
                    }
                    
                    return jsonify({
                        'status': 'executed',
                        'device_id': device_id,
                        'message': 'First command executed for new device',
                        'success': success
                    })
                
                # 기존 디바이스 처리
                last_timestamp = device_states.get(device_id, {}).get('last_timestamp', 0)
                time_diff = current_timestamp - last_timestamp
                
                if time_diff < 120:  # 2분 미만: 타이머 리셋
                    # 이전 상태 백업
                    previous_command = device_states[device_id].get('last_command')
                    os.environ["ifId"]=device_id
                    
                    # 상태 업데이트
                    device_states[device_id].update({
                        'last_timestamp': current_timestamp,
                        'last_command': command,
                        'status': 'pending',
                        'previous_command': previous_command
                    })
                    
                    # 2분 타이머 재설정
                    job_id = schedule_execution(device_id, command)
                    device_states[device_id]['job_id'] = job_id
                    logger.info(f"Device {device_id}: Timer reset with new command. Previous: {previous_command}")
                    return jsonify({
                        'status': 'scheduled',
                        'device_id': device_id,
                        'message': 'Command scheduled, timer reset for 2 minutes',
                        'execution_time': (now + timedelta(minutes=2)).isoformat()
                    })
                else:
                    # 2분 초과: 즉시 실행
                    success = execute_command(device_id, command)
                    logger.info(f"Device {device_id}: Executed after 2 minutes timeout")
                    
                    # 상태는 자동 초기화됨 (execute_command에서 처리)
                    return jsonify({
                        'status': 'executed',
                        'device_id': device_id,
                        'message': 'Command executed after timeout',
                        'success': success
                    })
                    
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            return jsonify({'error': str(e)}), 500

# 디버그용 상태 확인 엔드포인트
@app.route('/debug/states', methods=['GET'])
def debug_states():
    with global_lock:
        return jsonify({
            device_id: {
                'job_id': state.get('job_id'),
                'status': state.get('status'),
                'last_command': state.get('last_command'),
                'last_timestamp': state.get('last_timestamp'),
            }
            for device_id, state in device_states.items()
        })

@app.route('/debug/scheduler', methods=['GET'])
def debug_scheduler_jobs():
    jobs = scheduler.get_jobs()
    job_list = [{
        'id': job.id,
        'next_run_time': str(job.next_run_time),
        'args': job.args
    } for job in jobs]
    return jsonify(job_list)

@app.route('/debug/shutdown', methods=['GET'])
def debug_shutdown():
    try:
        scheduler.shutdown()
        logger.info("Scheduler shutdown successfully")
        return jsonify({'status': 'success', 'message': 'Scheduler shut down'})
    except Exception as e:
        logger.error(f"Error shutting down scheduler: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False)  # 다중 스레드 지원
