# _*_ coding: utf-8 _*_
from . import controller
from flask_wtf import FlaskForm
from flask import render_template,session,redirect,url_for,flash
from wtforms import StringField, SubmitField,DateTimeField
from wtforms.validators import required






#from wtforms.fields.html5 import DateField
from .. import db
from ..models.Appointment import Appointment
from flask_login import login_required



class CreateForm(FlaskForm):
    name = StringField('Call Name:',validators=[required()])

    time = DateTimeField('Call Time:',format='%Y-%m-%d %H:%M:%S')
    #time = StringField('Call Time:', validators=[required()])
    number = StringField('Call Phone Number:', validators=[required()])
    submit = SubmitField('Submit')

@controller.route('/create',methods=['GET','POST'])
@login_required
def create():
    name =  None
    form = CreateForm()
    #appointment = Appointment(call_name,call_time,number_called)
    if form.validate_on_submit():
        flash('Success! Your wake up call has been scheduled.')
        #appointment.call_name = form.name.data
        #appointment.number_called = form.number.data
        #appointment.call_time = "1990-02-02 12:25"
        appointment = Appointment(form.name.data,form.time.data,form.number.data)
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('controller.create'))
    return render_template('create.html', form=form, name=name)

    # print(db.session)
    # name = form.name.data
    # form.name.data = ''

        #return redirect(url_for('create'))
