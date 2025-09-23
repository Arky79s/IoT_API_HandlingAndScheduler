from flask import Flask,render_template,url_for,request
from API_Make_Token  import TokenIssuer
from API_Refrash import TokenRefresher
import os
import requests

from datetime import datetime, date, timedelta
import psycopg2
import pandas as pd


from dotenv import load_dotenv
from src.control import setRemoteControlFunc

import json

# Flask 객체 선언
app = Flask(__name__)
app.debug = True

#conn=psycopg2.connect(host="localhost", dbname='connecterDB', user='postgres',password='0930',port='5432')
conn=psycopg2.connect(host="localhost", dbname='connecterDB', user='postgres',password='0930')
cur= conn.cursor()

try:
    #cur.execute("Select * from public.test_history_table")
    cur.execute("insert into public.test_history_table(device_id,created_at) values('eb0e62e2f8da24a3dcki0w',now())")
    conn.commit()


except Exception as e:
    print(f"예외처리됨 : {e}") #@app.route('/posts', methods = ['POST']) 처럼 에러 명시하는편이 좋음
    
    conn.rollback()
finally:
#db접근 끝나면 커서와 커넥션을 닫아줌
    cur.close()
    conn.close()


@app.route("/")
def f1_server():
    return "f1_server run"

