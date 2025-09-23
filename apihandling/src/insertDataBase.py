import psycopg2

 

def recoder2DB(infoData,succeedFlag):

    #conn=psycopg2.connect(host="localhost", dbname='connecterDB', user='postgres',password='0930',port='5432')
    conn=psycopg2.connect(host = "localhost", dbname = 'connecterDB', user = 'postgres',password = '0930')
    cur= conn.cursor()

    try:
        #cur.execute("Select * from public.test_history_table")
        cur.execute(f"insert into recoder_history_table(created_at,info_data) values(now(),'{str(infoData)}')")
        #cur.execute("insert into recoder_history_table(created_at,info_data) values(now}")

        conn.commit()
    #INSERT INTO public.recoder_history_table(created_at, info_data) VALUES (now(), 'T28');

    except Exception as e:
        print(f"예외처리됨+{__name__}: {e}") #@app.route('/posts', methods = ['POST']) 처럼 에러 명시하는편이 좋음
        
        conn.rollback()
        return False
    finally:
    #db접근 끝나면 커서와 커넥션을 닫아줌
        cur.close()
        conn.close()

    return True


def recoder2DataBase(device_id,infoData,succeedFlag):
    
    #conn=psycopg2.connect(host="localhost", dbname='connecterDB', user='postgres',password='0930',port='5432')
    conn=psycopg2.connect(host = "localhost", dbname = 'connecterDB', user = 'postgres',password = '0930')
    cur= conn.cursor()

    try:
        #cur.execute("Select * from public.test_history_table")
        cur.execute(f"insert into public.history_save_table(device_id,execution_time,execution_type) values ('{device_id}',now(),'{str(infoData)}')")
        

        conn.commit()
    #INSERT INTO public.recoder_history_table(created_at, info_data) VALUES (now(), 'T28');

    except Exception as e:
        print(f"예외처리됨+{__name__}: {e}") #@app.route('/posts', methods = ['POST']) 처럼 에러 명시하는편이 좋음
        
        conn.rollback()
        return False
    finally:
    #db접근 끝나면 커서와 커넥션을 닫아줌
        cur.close()
        conn.close()

    return True
