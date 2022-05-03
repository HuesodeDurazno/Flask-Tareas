import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions



def get_db():
    #* G es un diccionario global
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE'],
        )
        
        #* Cursor para ejecutar instrucciones
        g.c = g.db.cursor(dictionary=True)

    return g.db,g.c

def close_db(e=None):
    #* Cierra la conexion con la base de datos despues de cada ejecucion
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    #* Ejecutamos las instrucciones	
    #* Conexion a la base de datos
    db,c = get_db()
    for i in instructions:
        c.execute(i)
    db.commit()

#* Definimos comando para inicializar la base de datos
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

#* Al iniciar la app agregamos el cierre de la conexion a la base de datos en cada peticion y agregamos el comando de inicializacion de la base de datos
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)