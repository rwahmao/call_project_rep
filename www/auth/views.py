# _*_ coding: utf-8 _*_

from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required
from . import auth
from .. import db
from .forms import LoginForm,RegistrationForm
from ..models.models import User



@auth.route('/login',methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            #uu = load_user(user.is_active)
            #flash(__dict__(user.email.count))
            #flash(print(user.is_active))
            flash('Hi.Thank you for join the community.Before use our service,you have to verify your phone number first,try to click here to start.')
            return redirect(request.args.get('next') or url_for('controller.create'))
        flash('Error.Invalid username or password.')
    return render_template('/login.html', form=form)


@auth.route('/logout',methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('/register.html', form=form)