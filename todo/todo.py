from flask import Blueprint, flash, g,redirect,render_template,request,url_for

from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo',__name__)

@bp.route('/')
@login_required
def index():
    db,c = get_db()
    c.execute('SELECT t.id, t.description,u.username,t.completed,t.created_at FROM todo t JOIN user u ON t.created_by = u.id WHERE t.created_by = u.id ORDER BY t.created_by DESC')
    todos =  c.fetchall()
    
    return render_template('todo/index.html',todos=todos)

@bp.route('/create',methods=('GET','POST'))
@login_required
def create():
    return render_template('todo/create.html')

@bp.route('/<int:id>/update',methods=('GET','POST'))
@login_required
def update():
    pass