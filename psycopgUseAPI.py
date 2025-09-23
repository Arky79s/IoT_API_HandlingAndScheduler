import psycopg2
from psycopg2.extras import RealDictCursor

def connect_with_psycopg2():
    try:
        # 연결 설정
        connection = psycopg2.connect(
            host="localhost",        # 또는 실제 호스트 주소
            database="your_db_name", # 데이터베이스 이름
            user="your_username",    # 사용자명
            password="your_password", # 비밀번호
            port="5432"             # PostgreSQL 기본 포트
        )
        
        # 딕셔너리 형태로 결과 받기
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        # 쿼리 실행
        cursor.execute("SELECT * FROM your_table_name LIMIT 10")
        records = cursor.fetchall()
        
        for record in records:
            print(record)
            
        return records
        
    except Exception as error:
        print(f"PostgreSQL 연결 오류: {error}")
    
    finally:
        if connection:
            cursor.close()
            connection.close()
