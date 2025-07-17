from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import re

app = Flask(__name__, template_folder='templates', static_folder='static')


database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)


app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'postgresql://pawfect_db_user:Bb8XbtoCWJV5mTKLw0FcE1tvKkUloeYR@dpg-d1saoeumcj7s73dgnqtg-a/pawfect_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Pet {self.name}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

@app.route('/pets')
def list_pets():
    pets = Pet.query.all()
    return render_template('pets.html', pets=pets)

@app.route('/adopt')
def adopt():
    return render_template('adopt.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)