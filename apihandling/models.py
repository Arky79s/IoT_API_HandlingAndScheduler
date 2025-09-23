from apihandling import db



#class Phishing(db.Model) :
    #생성예시
    # __tablename__ = 'phishings'

    # id = db.Column(db.Integer, primary_key=True)
    # url = db.Column(db.String())
    # timestamp = db.Column(db.DateTime, default = db.func.current_timestamp())

    # def __init__(self, url) :
    #     self.url = url

    # def save(self) :
    #     db.session.add(self)
    #     db.session.commit()

    # @staticmethod
    # def get_all() :
    #     return Phishing.query.all()

    # def __repr__(self) :
    #     return f"<ID {self.id}  , URL {self.url}>"




# class HistoryRecode(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # id 속성을 기본 키(Primary Key)로 만듦
#     subject = db.Column(db.String(200), nullable=False) # nullable은 빈값 허용할지 여부, False면 허용x
#     content = db.Column(db.Text(), nullable=False)
#     create_date = db.Column(db.DateTime(), nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id 속성을 기본 키(Primary Key)로 만듦
    subject = db.Column(db.String(200), nullable=False) # nullable은 빈값 허용할지 여부, False면 허용x
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

# class Answer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
#     question = db.relationship('Question', backref=db.backref('answer_set'))
#     content = db.Column(db.Text(), nullable=False)
#     create_date = db.Column(db.DateTime(), nullable=False)