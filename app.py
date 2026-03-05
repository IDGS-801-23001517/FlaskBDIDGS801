from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db
from flask_migrate import Migrate
from maestros.routes import maestros
from alumnos.routes import alumnos
from cursos.routes import cursos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(maestros)
app.register_blueprint(alumnos)
app.register_blueprint(cursos)

migrate = Migrate(app, db)
csrf = CSRFProtect(app)
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)