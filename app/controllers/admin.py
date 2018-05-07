from flask import render_template, session, request, flash, redirect, url_for
from functools import wraps
from app import app
import os

from app.models.users import Users
from app.models.sensors import Sensors
from app.models.data import Data

USERNAME = os.environ['ADMIN_USERNAME']
PASSWORD = os.environ['ADMIN_PASSWORD']

def admin_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if not session.get('is_admin'):
            flash('Admin credential is required!','danger')
            return redirect(url_for('admin_login'))
        return func(*args, **kwargs)
    return wrapper


@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['admin']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid Admin credentials!','danger')
            return redirect(url_for('admin_login'))
    else:
        return render_template('admin/login.html')



@app.route('/admin')
@admin_required
def admin():
    users = Users.objects.all()
    sensors = Sensors.objects.all()
    data = Data.objects.all()
    devices = set()
    for i in data:
        devices.add(i.device)
    return render_template(
                            'admin/index.html',
                            users=users,
                            sensors=sensors,
                            data=data,
                            devices=devices
                            )



@app.route('/admin/logout')
def admin_logout():
    session['is_admin'] = False
    return redirect(url_for('login'))