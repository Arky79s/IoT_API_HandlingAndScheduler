from psycopg2 import pool
import os

import psycopg2  #
from psycopg2.extras import RealDictCursor


class PostgreSQLPool:
    def __init__(self):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,  # 최소 1개, 최대 20개 연결
            host="localhost",
            database=os.getenv('PG_DB'),
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASSWORD'),
            port=os.getenv('PG_PORT' or '5432')
        )
    
    def execute_query(self, query, params=None):
        connection = None
        try:
            connection = self.connection_pool.getconn()
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.rowcount
                
        except Exception as error:
            if connection:
                connection.rollback()
            print(f"쿼리 실행 오류: {error}")
        
        finally:
            if connection:
                cursor.close()
                self.connection_pool.putconn(connection)

# 사용 예시
if __name__ == "__main__":
    # 방법 선택해서 사용
    
    # 1. 직접 연결
    #connect_with_psycopg2()
    
    # 2. SQLAlchemy
    # connect_with_sqlalchemy()
    
    # 3. Flask 앱 실행 시
    # flask_sqlalchemy_example()
    
    # 4. 연결 풀 사용
    # db_pool = PostgreSQLPool()
    # result = db_pool.execute_query("SELECT * FROM your_table_name LIMIT 5")
    # print(result)
    
    print("PostgreSQL 연결 코드 준비 완료!")