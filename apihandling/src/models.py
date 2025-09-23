
from apihandling import db

class Recoding(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id 속성을 기본 키(Primary Key)로 만듦
    remoteInfo = db.Column(db.Text(), nullable=False)
    create_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id 속성을 기본 키(Primary Key)로 만듦
    remoteInfo = db.Column(db.Text(), nullable=False)
    create_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)


# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
#     question = db.relationship('Question', backref=db.backref('answer_set'))
#     content = db.Column(db.Text(), nullable=False)
#     create_date = db.Column(db.DateTime(), nullable=False)