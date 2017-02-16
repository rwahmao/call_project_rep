# _*_ coding: utf-8 _*_
from . import controller
from flask_wtf import FlaskForm
from flask import render_template,session,redirect,url_for,flash,request
from wtforms import StringField, SubmitField,DateTimeField,BooleanField
from wtforms.validators import required
from twilio.rest import TwilioRestClient






#from wtforms.fields.html5 import DateField
from .. import db
from ..models.models import Number
from flask_login import login_required,current_user
from flask_sqlalchemy import SQLAlchemy


class addNumberForm(FlaskForm):
    name = StringField('Name:',validators=[required()])
    #time = StringField('Call Time:', validators=[required()])
    number = StringField('Call Phone Number:', validators=[required()])
    sms = BooleanField('SMS Available',default='false')
    submit = SubmitField('Submit')

class verifyNumberForm(FlaskForm):
    #time = StringField('Call Time:', validators=[required()])
    number = StringField('Verify Code：', validators=[required()])
    submit = SubmitField('Submit')



@controller.route('/addnumber',methods=['GET','POST'])
@login_required
def addNumber():
    flash('After clicking the Add Phone Number button, '
          'you will get a 4-digit number by phone or sms, '
          'You must verify this phone number before you can schedule calls to it.')
    form = addNumberForm()
    #1.save the number
    if form.validate_on_submit():
        uid = current_user.get_id()
        number_info = Number()
        number_info.name = form.name.data
        number_info.number = form.number.data
        number_info.sms = form.sms.data
    # 2.link the number to current user
        number_info.user_id = uid
        db.session.add(number_info)
        db.session.commit()
    # 3.trigger send code and jump to verify phone number page
        #3.1 generate a random number
        import random
        session.verify_code = random.randint(1000,9999)
        print(session.verify_code+11)
        #3.2 send to user phone via sms if user checked sms avaiblable
        from ..setting import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,TWILIO_NUMBER
        client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        #client.messages.create(
        #    to='9095590969',
        #   from_= TWILIO_NUMBER,
        #   body= session.verify_code,
        #)
        # 3.3 call and read code to user phone via phone call if user unchecked sms avaiblable
        verify_code = str(session.verify_code)
        thousand = verify_code[0]
        hundred = verify_code[1]
        thi = verify_code[2]
        dem = verify_code[3]
        str1 = 'http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSay%3EHello+There.+Verify+Code+is,'
        str2 = '.+%3C%2FSay%3E%3C%2FResponse%3E'
        urlstr = str1 + thousand + '+' + hundred + '+' + thi + '+' + dem + str2
        """
        call = client.calls.create(to= "+19095590969",  # Any phone number
                                   from_= TWILIO_NUMBER,  # Must be a valid Twilio number
                                   url= urlstr
                                   )
        """

        vform = verifyNumberForm()

        return render_template('verifyphonenumber.html',form = vform)

    #3.trigger send code and jump to verify phone number page


    return render_template('addnumber.html',form = form)



@controller.route('/verify',methods=['GET','POST'])
@login_required
def VerifyCode():
    print(session.verify_code)
    pass
