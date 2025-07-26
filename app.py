from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import requests

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

# -------------------------------
# Initialize Flask app
# -------------------------------
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'a8f3@9!gks92&x1z'

# -------------------------------
# Database configuration
# -------------------------------
database_url = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
if database_url.startswith("postgres://"):
    # Fix for SQLAlchemy compatibility with Heroku-style URLs
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------------
# Database Models
# -------------------------------
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

# -------------------------------
# Create database tables if not exist
# -------------------------------
with app.app_context():
    db.create_all()

# -------------------------------
# Helper function to fetch dog facts
# -------------------------------
def get_dog_facts(limit=3):
    try:
        response = requests.get(f"https://dogapi.dog/api/v2/facts?limit={limit}")
        if response.status_code == 200:
            data = response.json()
            return [item['attributes']['body'] for item in data.get('data', [])]
    except Exception as e:
        print("Error fetching dog facts:", e)
    # Fallback facts if API fails
    return [
        "All my dogs were named Charlie",
        "Dogs can learn over 1000 words",
        "They dream just like humans!"
    ]

# -------------------------------
# Inject dog facts into all templates
# -------------------------------
@app.context_processor
def inject_dog_facts():
    return {'dog_facts': get_dog_facts()}

# -------------------------------
# Routes / Views
# -------------------------------

# Home page with contact form and steps
@app.route('/', methods=['GET', 'POST'])
def index():
    steps = [
        {
            "title": " Reach out to us",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        },
        {
            "title": " Find your pet",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        },
        {
            "title": " Have A Meeting",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        }
    ]

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'
        flash('Thank you for contacting us!!')
        return render_template('index.html', form_action=url_for('index'), first_name=first_name, surname=surname, email=email, message=message, terms=terms, steps=steps)
    
    return render_template('index.html', steps=steps, form_action=url_for('index'))

# Pets listing page
@app.route('/pets')
def list_pets():
    pets = Pet.query.all()
    if not pets:
        pets = [
            Pet(img='images/Golden-Retriever.png', name='Charlie', age=3, breed='Golden Retriever', species='Dog'),
        ]
        for pet in pets:
            db.session.add(pet)
        db.session.commit()
        pets = Pet.query.all()
    return render_template('pets.html', pets=pets)

# Adoption information page
@app.route('/adopt')
def adopt():
    return render_template('adopt.html')

# About page with multiple sections
@app.route('/about', methods=['GET', 'POST'])
def about():
    sections = [
        {
            'image': "images/woman.png",
            'alt': 'woman and dog',
            'title': 'From A Dream',
            'paragraphs': [
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
            ],
            'reverse': False
        },
        {
            'image': "images/bulldog.png",
            'alt': 'woman and dog',
            'title': 'From A Dream',
            'paragraphs': [
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
            ],
            'reverse': True
        },
        {
            'image': "images/man.png",
            'alt': 'woman and dog',
            'title': 'From A Dream',
            'paragraphs': [
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
            ],
            'reverse': False
        },
    ]

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'
        flash('Thank you for contacting us!!')
        return render_template(
            'about.html',
            form_action=url_for('about'),
            first_name=first_name,
            surname=surname,
            email=email,
            message=message,
            terms=terms,
            sections=sections
        )

    return render_template(
        'about.html',
        form_action=url_for('about'),
        sections=sections
    )

# Contact page with form that saves submission to DB
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

# FAQ page with contact form (stores submissions)
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



# -------------------------------
# Run the app
# -------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
