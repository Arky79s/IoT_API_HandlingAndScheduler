
# 3. Flask-SQLAlchemy를 사용하는 경우 (PyBo 스타일)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 모델 정의 예시
class YourModel(db.Model):
    __tablename__ = 'your_table_name'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

def flask_sqlalchemy_example():
    with app.app_context():
        # 데이터 조회
        records = YourModel.query.all()
        for record in records:
            print(f"ID: {record.id}, Name: {record.name}, Email: {record.email}")
        
        # 조건부 조회
        specific_record = YourModel.query.filter_by(name='특정이름').first()
        if specific_record:
            print(f"찾은 레코드: {specific_record.name}")
