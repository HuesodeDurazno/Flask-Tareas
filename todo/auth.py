import functools
import re

from flask import (Blueprint, blueprints, flash,g, redirect,render_template,request,url_for,session)

from werkzeug.security import check_password_hash,generate_password_hash

from todo.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        db,c = get_db()
        error = None
        c.execute('SELECT * FROM user WHERE username = %s',(username,))
        if not username:
            error = 'Username is required.'
        if  not password:
            error = 'Password is required.'
        elif c.fetchone() is None:
            error = 'User {} is already registered.'.format(username)
        
        if error is None:
            c.execute('INSERT INTO user (username,password) VALUES (%s,%s)',(username,generate_password_hash(password)))
            db.commit()
        
        return redirect(url_for('auth.login'))
    
    flash(error)
    
    return render_template('auth/register.html')

@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db,c = get_db()
        error = None
        c.execute('SELECT * FROM user WHERE username = %s',(username,))
        user = c.fetchone()
        
        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user['password'],password):
            error = 'Incorrect username or password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)
    
    return render_template('auth/login.html')