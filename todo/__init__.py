import os 
from flask import Flask

def create_app():
    
    #* Creamos la aplicacion Flask
    app = Flask(__name__)
    
    
    #*Obtenemos variables de entorno
    app.config.from_mapping(
        SECRET_KEY="SUPER_SECRET_KEY", 
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE'),
        )
    
    #* Importamos Archivo db
    from . import db
    
    #* Inicializamos la base de datos
    db.init_app(app)
    
    from . import auth
    
    app.register.blueprint(auth.bp)
    
    #*Definimos ruta hola
    @app.route('/hola')
    def hola():
        return 'Hola mundo'
    
    return app