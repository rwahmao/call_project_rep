# _*_ coding: utf-8 _*_
# Download the Python helper library from twilio.com/docs/python/install
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import TwilioRestClient
import datetime,time

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('www.setting')

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    call_name = db.Column(db.String(10))
    call_time = db.Column(db.DateTime())
    number_called = db.Column(db.String(10))

    def __init__(self,call_name,call_time,number_called):
       self.call_name = call_name
       self.call_time = call_time
       self.number_called = number_called

    def __repr__(self):
        return '<User %r>' % self.call_name

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACfd8d026acbc17c52773ade4c1444aa4f"
auth_token  = "c6118fbd39a771a0524d430ed5298dab"
client = TwilioRestClient(account_sid, auth_token)

while True:
#if True:

    format = '%Y-%m-%d %H:%M:%S'
    now = datetime.datetime.strptime(time.strftime(format),format)
    #now = time.time()
    print(now)
    #ctime = '2017-02-09 15:13:00'
    c_count = Appointment.query.filter_by(call_time=now).count()
    print(c_count)
    #c_time = Appointment.query.filter_by(id=26).first()
    #print(c_time.call_time)

    if c_count is not None and c_count:
        appointment = Appointment.query.filter_by(call_time=now).all()
        for i in appointment:
            print(i.number_called + ' was called ')
            #call = client.calls.create(url="http://www.flyingsaucervoy.com/twilio/voice.xml", to=i.number_called,
            #                           from_="+12132495051")

    time.sleep(1)

#alarmAtTimestamp = int(time.mktime(time.strptime(alarmAt, format)))
#while True:
#    now = int(time.time())
#   if now == alarmAtTimestamp:
#call = client.calls.create(url="http://www.flyingsaucervoy.com/twilio/voice.xml",to="+19095590969",from_="+12132495051")
#print('5051_called')
#call_again = client.calls.create(url="http://www.flyingsaucervoy.com/twilio/voice.xml",to="+19095590969",from_="+12132495051")
#print('0969_called')
#time.sleep(1)