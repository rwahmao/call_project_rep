# _*_ coding: utf-8 _*_
from . import controller
from flask_wtf import FlaskForm
from flask import render_template,session,redirect,url_for,flash,request
from wtforms import StringField, SubmitField,DateTimeField
from wtforms.validators import required






#from wtforms.fields.html5 import DateField
from .. import db
from ..models.Appointment import Appointment
from flask_login import login_required,current_user
from flask_sqlalchemy import SQLAlchemy


class CreateForm(FlaskForm):
    name = StringField('Call Name:',validators=[required()])

    time = DateTimeField('Call Time:',format='%Y-%m-%d %H:%M',validators=[required()])
    #time = StringField('Call Time:', validators=[required()])
    number = StringField('Call Phone Number:', validators=[required()])
    submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
    name = StringField('Call Name:',validators=[required()])

    time = DateTimeField('Call Time:',format='%Y-%m-%d %H:%M')
    #time = StringField('Call Time:', validators=[required()])
    number = StringField('Call Phone Number:', validators=[required()])
    submit = SubmitField('Update')

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
        uid = current_user.get_id()
        appointment = Appointment(form.name.data,form.time.data,form.number.data, uid)
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('controller.listCall'))
    return render_template('create.html', form=form, name=name)

    # print(db.session)
    # name = form.name.data
    # form.name.data = ''

        #return redirect(url_for('create'))




@controller.route('/call',methods=['GET','POST'])
@login_required
def listCall():

    uid = current_user.get_id()
    calllist = Appointment.query.filter_by(user_id = uid).all()
    #print(c_count)
    # c_time = Appointment.query.filter_by(id=26).first()
    # print(c_time.call_time)


    return render_template('call.html',calllist=calllist)

@controller.route('/suspend/<int:call_id>',methods=['GET','POST'])
@login_required
def suspendCall(call_id):
    flash('Success. Your had suspended your reminder call.')
    print(call_id)

    my = Appointment.query.filter_by(id = call_id).first()
    my.call_status = 0

    #print(my.count())
    #appointment.call_status = 1
    #db.session.add(my)
    db.session.commit()

    uid = current_user.get_id()
    calllist = Appointment.query.filter_by(user_id = uid).all()
    return render_template('call.html',calllist=calllist)
    #return render_template('call.html')

@controller.route('/activate/<int:call_id>',methods=['GET','POST'])
@login_required
def activateCall(call_id):
    flash('Success. Your had activated your reminder call.')
    print(call_id)
    my = Appointment.query.filter_by(id = call_id).first()
    my.call_status = 1
    #print(my.count())
    #appointment.call_status = 1
    #db.session.add(my)
    db.session.commit()

    uid = current_user.get_id()
    calllist = Appointment.query.filter_by(user_id = uid).all()
    return render_template('call.html',calllist=calllist)
    #return render_template('call.html')


@controller.route('/edit/<int:call_id>',methods=['GET','POST'])
@login_required
def editCall(call_id):

    name = None
    form = UpdateForm()
    #flash(form.errors)
    #print(form.name.data)
    #print('abcd')
    #print(form.time.data)
    #print(form.number.data)
    #注意这个因为默认取不到js控制的时间input框的值（不点一下time值永远是none，通不过validator，所以取消的安全措施）
    if request.method == "POST":
        flash('Success. Your had updated your reminder call settings.')
        #appointment.call_name = form.name.data
        #appointment.number_called = form.number.data
        #appointment.call_time = "1990-02-02 12:25"
        #print(call_id)
        appointment = Appointment.query.filter_by(id = call_id).first()
        appointment.call_name = form.name.data
        if form.time.data != None:
            appointment.call_time = form.time.data
        appointment.number_called = form.number.data
        db.session.commit()
        return redirect(url_for('controller.listCall'))
    form = UpdateForm()
    my = Appointment.query.filter_by(id=call_id).first()
    return render_template('edit.html', form=form, name=name,my=my)

@controller.route('/delete/<int:call_id>',methods=['GET','POST'])
@login_required
def deleteCall(call_id):
    flash('Success. Your had Delete your scheduled call.')
    my = Appointment.query.filter_by(id = call_id).first()
    db.session.delete(my)
    db.session.commit()
    uid = current_user.get_id()
    calllist = Appointment.query.filter_by(user_id = uid).all()
    return render_template('call.html',calllist=calllist)
    #return render_template('call.html')