from flask import Flask, make_response, request, Response , jsonify
from flask import Blueprint

import requests
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, date, timedelta
from flask_migrate import Migrate

from apihandling import create_app,db
#import db

import psycopg2
import pandas as pd




#bp = Blueprint('question', __name__, url_prefix='/question')


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<postgres>:<0930>@localhost:5432/<database>'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
app=create_app()
migrate = Migrate(app, db)


# 커넥션 만들기 (파이썬과 포스트그레스 connect)
conn = psycopg2.connect(host='localhost',dbname='connecterDB',user='postgres',password='0930', port='5432')

# 커서 만들기
# 커서 객체는 실질적으로 DB에 쿼리문을 수행하고, 결과를 가져오는 역할을 함
cur = conn.cursor()

# 커서로 쿼리문 수행
#cur.execute('INSERT INTO f1_fasoo (id, name, task_name, create_date, working_time) VALUES (3, \'손호준\', \'인턴 프로젝트\', \'2022-12-01\', 24)')
#cur.execute('CREATE TABLE TEST_TABLE2( id SERIAL PRIMARY KEY, CREATE_ON TIMESTAMP NOT NULL);')

cur.execute('SELECT * FROM public.test_hisory_table')

# 포스트그레스로 값을 전달하려면 커밋
# conn.commit()

# execute는 말 그대로 쿼리문을 실행하는 것. 실제로 해당 트랜잭션이 수행되려면 commit을 통해 DB에 반영해야 한다.

# 커서로 결과 가져와서 info에 저장
info = cur.fetchall()
df = pd.DataFrame(info)
print(df)

#db접근 끝나면 커서와 커넥션을 닫아줌
cur.close()
conn.close()

@app.route("/")
def f1_server():
    return "f1_server run"