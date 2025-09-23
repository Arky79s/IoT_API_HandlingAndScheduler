
작업 완료 이후 정리는X  
MVC 패턴까지는 아니더라도 라우터표기를 컨트롤러나 다른곳에 참조해서 불러오도록  
쓰레드 락까지는 필요 없었음 #주석 상세히 #리드미파일 부적인 파일 생성

지금 구조로는 인터벌 스케줄러 하나만 하고 작동 펑션만 2분 마다 구동 하도록 해야하는데 그러진않았습.
 인터벌로  디바이스 스테이터스 오브젝트 리스트 ,즉 파이썬에서  딕트 리스트  list(dict )

아래 방식
 [{ key1:vale, key2:value2  }]
으로 사용 


하여 진행할것이고 메인 구분 키를 device ID 로 잡명칭은 exc_디바이스 아이디로 되도록 표준화할것 


single device 가 끝나면 Multi Device로 다중제어 가능한 구조로 완성할수 있도록할것 


modle.py 에서 모델 활용은 적어서 아쉬웠습 DTO 구조를 추가하는것은 아니더라도 

라우터에서 코드 활용은 자제할것 요망 # 컨트롤단에서 빼고 라우팅은 Post 로도  헤더 바디로  받고 리턴값 받는것으로 최소화하여야 하는데 너무 많음 





API_IoTControl_TempCheack.py 

IoT 컨트롤 핸들링 파일 


토큰 생성 및 재발급 

routes_refactory.py 

flask 진자 템플릿에 영향이 커서 비동기 사용이 제한적일수 있음 

src 는 안에서 작동이 안되어 밖으로 빼냄 


routes_refactory_3rd Scheduler_singleDevice coplete copy 2.py
routes_refactory_3rd Scheduler_singleDevice beforeCoplete Last_Grok ver_proto.py
마지막 진행 파일들임. 


GPT나 １