from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'a8f3@9!gks92&x1z'

database_url = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1) 

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
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

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    terms = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Submission {self.first_name} {self.surname}>'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'
        flash('Thank you for contacting us!!')
        return render_template('index.html', form_action=url_for('index'), first_name=first_name, surname=surname, email=email, message=message, terms=terms)
    return render_template('index.html', form_action=url_for('index'))

@app.route('/pets')
def list_pets():
    pets = Pet.query.all()
    return render_template('pets.html', pets=pets)

@app.route('/adopt')
def adopt():
    return render_template('adopt.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'
        flash('Thank you for contacting us!!')
        return render_template('about.html', form_action=url_for('about'), first_name=first_name, surname=surname, email=email, message=message, terms=terms)
    return render_template('about.html', form_action=url_for('about'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'
        submission = Submission(first_name=first_name, surname=surname, email=email, message=message, terms=terms)
        db.session.add(submission)
        db.session.commit()
        flash('Thank you for contacting us!!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/faq', methods=['GET', 'POST'])
def faq():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'
        submission = Submission(first_name=first_name, surname=surname, email=email, message=message, terms=terms)
        db.session.add(submission)
        db.session.commit()
        flash('Thank you for contacting us!!')
        return render_template('faq.html', form_action=url_for('faq'), first_name=first_name, surname=surname, email=email, message=message, terms=terms)
    return render_template('faq.html', form_action=url_for('faq'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
