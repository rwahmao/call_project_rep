from www import db

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    call_name = db.Column(db.String(10))
    call_time = db.Column(db.DateTime(20))
    number_called = db.Column(db.String(10))

    def __init__(self,call_name,call_time,number_called):
       self.call_name = call_name
       self.call_time = call_time
       self.number_called = number_called

    def __repr__(self):
        return '<User %r>' % self.call_name