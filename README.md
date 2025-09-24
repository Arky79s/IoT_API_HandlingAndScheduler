# IoT Device Control API System

## 📌 프로젝트 개요

이 프로젝트는 **IoT 디바이스 상태 확인 및 제어를 위한 API 시스템**입니다.  
플라스크(Flask)를 기반으로 하며, 향후 다중 디바이스 제어(Multi-Device Control)를 지원할 수 있도록 구조화되어 있습니다.  

- **기본 동작**:  
  2분 간격 인터벌 스케줄러로 디바이스 상태 확인  
- **데이터 포맷**:  
  `list[dict]` 형태의 디바이스 상태 객체  
  ```python
  [
      {"device_id": "exc_0001", "status": "ON", "temp": 23.5},
      {"device_id": "exc_0002", "status": "OFF", "temp": 19.0}
  ]


⚙️ 프로젝트 구조
  /project-root
│
├── src/
│   ├── model.py                # (활용도 낮음) 모델 정의 파일
│   ├── controller/             # 제어 로직 담당
│   │   ├── iot_controller.py   # 실제 디바이스 핸들링 로직
│   └── scheduler/
│       └── interval_runner.py  # 2분 간격 인터벌 스케줄러
│
├── routes/
│   ├── routes_refactory.py                       # 주요 라우팅 처리 파일
│   ├── routes_refactory_3rd Scheduler_singleDevice beforeCoplete Last_Grok ver_proto.py
│   └── routes_refactory_3rd Scheduler_singleDevice coplete copy 2.py
│
├── API_IoTControl_TempCheack.py     # IoT 제어 핸들링 및 토큰 처리 파일
│
├── requirements.txt
└── README.md


[
  { "device_id": "exc_001", "status": "on", "temp": 22.5 },
  { "device_id": "exc_002", "status": "off", "temp": 18.2 }
]
📑 핵심 구현 사항
✅ 라우팅 처리

모든 라우팅은 routes_refactory.py 또는 해당 리팩토링 파일을 통해 관리

라우터에서 직접 로직 구현 ❌ → 컨트롤러 참조 방식으로 리팩토링 필수

불필요한 DTO 구조는 사용하지 않되, 정리된 입력/출력 처리 권장

POST 방식 + Header/Body 사용하여 정리된 통신 지향

✅ 스케줄러

현재 구조는 단일 디바이스(single device) 대상 스케줄링만 작동

2분 간격(interval)으로 디바이스 상태 조회 및 처리 함수 실행

추후 multi device 구조로 확장 예정

device_id 기준으로 딕셔너리 리스트 관리

객체 명명 규칙: exc_<device_id> 형식

✅ 디바이스 상태 객체

표준화된 포맷 사용: list[dict]

메인 키: device_id

예시:
[
  { "device_id": "exc_001", "status": "on", "temp": 22.5 },
  { "device_id": "exc_002", "status": "off", "temp": 18.2 }
]



Flask Jinja 템플릿 사용 시 비동기 제약 있음

일부 src/ 내부 파일은 정상 작동하지 않아 루트 디렉터리로 이동함

최종 작동 기준 파일:

routes_refactory_3rd Scheduler_singleDevice beforeCoplete Last_Grok ver_proto.py

routes_refactory_3rd Scheduler_singleDevice coplete copy 2.py


| 날짜      | 내용                                |
| ------- | --------------------------------- |
| 2025.09 | Single Device 기준 스케줄링 구현 완료       |
| 예정      | Multi Device 확장 / 코드 모듈화 / 테스트 구축 |



---

### ✅ 참고

위 템플릿은 실제 코드 및 구조에 맞게 각 항목을 수정해 사용할 수 있습니다.  
특히 **파일 이름이 긴 경우**, 운영 시에는 일부 리팩토링을 통해 구분 가능한 네이밍으로 간소화하는 것이 유지보수에 좋습니다.

필요하다면 `requirements.txt`, `.env.example`, `start.sh` 등의 부수적 파일도 추가로 생성 가능합니다.

원하는 형식(한글 전체/영문 전체 등)이 있다면 조정해 드릴 수 있습니다.

