# -*- coding: utf-8 -*-
from www import app,db
from flask import redirect,url_for,render_template

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return redirect(url_for('auth.login'))
 #  return render_template('create-call.html')

if __name__ == '__main__':
    manager.run()
