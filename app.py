from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import requests

# -------------------------------
# Load Environment Variables
# -------------------------------

load_dotenv()

# -------------------------------
# Initialize Flask App
# -------------------------------

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'a8f3@9!gks92&x1z'

# -------------------------------
# Database Configuration
# -------------------------------

database_url = os.environ.get('DATABASE_URL', 'sqlite:///test.db')

# Adjust for deprecated postgres:// in Render
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------------
# Database Models
# -------------------------------

class Pet(db.Model):
    """Model representing a pet available for adoption."""
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Pet {self.name}>'

class Submission(db.Model):
    """Model representing a contact form submission."""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    terms = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Submission {self.first_name} {self.surname}>'

# -------------------------------
# Create Tables (if not exist)
# -------------------------------

with app.app_context():
    db.create_all()

# -------------------------------
# Helper: Fetch Dog Facts API
# -------------------------------

def get_dog_facts(limit=3):
    """Fetch a limited number of dog facts from an external API."""
    try:
        response = requests.get(f"https://dogapi.dog/api/v2/facts?limit={limit}")
        if response.status_code == 200:
            data = response.json()
            return [item['attributes']['body'] for item in data.get('data', [])]
    except Exception as e:
        print("Error fetching dog facts:", e)
    return [
        "All my dogs were named Charlie",
        "Dogs can learn over 1000 words",
        "They dream just like humans!"
    ]

# -------------------------------
# Context Processor: Inject Dog Facts
# -------------------------------

@app.context_processor
def inject_dog_facts():
    """Inject dog facts globally into all templates."""
    return {'dog_facts': get_dog_facts()}

# -------------------------------
# Route: Home Page
# -------------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    """Homepage with steps and contact form (not saved to DB)."""
    steps = [
        {"title": "Reach out to us", "description": "Lorem ipsum..."},
        {"title": "Find your pet", "description": "Lorem ipsum..."},
        {"title": "Have A Meeting", "description": "Lorem ipsum..."}
    ]

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'
        flash('Thank you for contacting us!!')

        return render_template('index.html', form_action=url_for('index'),
                               first_name=first_name, surname=surname,
                               email=email, message=message, terms=terms, steps=steps)

    return render_template('index.html', steps=steps, form_action=url_for('index'))

# -------------------------------
# Route: List Pets
# -------------------------------

@app.route('/pets')
def list_pets():
    """Displays a list of pets with filtering options."""
    from sqlalchemy import distinct

    if Pet.query.count() == 0:
        pets_available = [
            Pet(img='images/Golden-Retriever.png', name='Charlie', age=3, breed='Golden Retriever', species='Dog'),
            Pet(img='images/Beagle.png', name='Max', age=2, breed='Beagle', species='Dog'),
            # ... [more pets] ...
            Pet(img='images/VeiledChameleon.png', name='Echo', age=2, breed='Veiled Chameleon', species='Reptile'),
        ]
        db.session.bulk_save_objects(pets_available)
        db.session.commit()

    name = request.args.get('name', '').strip()
    age = request.args.get('age', '').strip()
    breed = request.args.get('breed', '').strip()
    species = request.args.get('species', '').strip()

    query = Pet.query
    if name:
        query = query.filter(Pet.name.ilike(f"%{name}%"))
    if age:
        try:
            query = query.filter(Pet.age == int(age))
        except ValueError:
            flash("Age must be a number", "filter")
    if breed:
        query = query.filter(Pet.breed.ilike(f"%{breed}%"))
    if species:
        query = query.filter(Pet.species == species)

    pets = query.all()
    species_options = [row[0] for row in db.session.query(distinct(Pet.species)).all()]

    return render_template('pets.html', pets=pets, name=name, age=age, breed=breed,
                           selected_species=species, species_options=species_options)

# -------------------------------
# Route: Adoption Page
# -------------------------------

@app.route('/adopt')
def adopt():
    """Displays information about the adoption process."""
    return render_template('adopt.html')

# -------------------------------
# Route: About Page
# -------------------------------

@app.route('/about', methods=['GET', 'POST'])
def about():
    """About us page with optional contact form."""
    sections = [
        {
            'image': "images/woman.png",
            'alt': 'woman and dog',
            'title': 'From A Dream',
            'paragraphs': ['Lorem ipsum...', 'Ut enim...'],
            'reverse': False
        },
        {
            'image': "images/bulldog.png",
            'alt': 'woman and dog',
            'title': 'From A Dream',
            'paragraphs': ['Lorem ipsum...', 'Ut enim...'],
            'reverse': True
        },
        {
            'image': "images/man.png",
            'alt': 'woman and dog',
            'title': 'From A Dream',
            'paragraphs': ['Lorem ipsum...', 'Ut enim...'],
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

        return render_template('about.html', form_action=url_for('about'),
                               first_name=first_name, surname=surname,
                               email=email, message=message, terms=terms, sections=sections)

    return render_template('about.html', form_action=url_for('about'), sections=sections)

# -------------------------------
# Route: Contact Page
# -------------------------------

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form that saves submission to the database."""
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'

        submission = Submission(first_name=first_name, surname=surname,
                                email=email, message=message, terms=terms)
        db.session.add(submission)
        db.session.commit()

        flash('Thank you for contacting us!!')
        return redirect(url_for('contact'))

    return render_template('contact.html')

# -------------------------------
# Route: FAQ Page
# -------------------------------

@app.route('/faq', methods=['GET', 'POST'])
def faq():
    """FAQ page with embedded contact form."""
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'

        submission = Submission(first_name=first_name, surname=surname,
                                email=email, message=message, terms=terms)
        db.session.add(submission)
        db.session.commit()

        flash('Thank you for contacting us!!')
        return render_template('faq.html', form_action=url_for('faq'),
                               first_name=first_name, surname=surname,
                               email=email, message=message, terms=terms)

    return render_template('faq.html', form_action=url_for('faq'))

# -------------------------------
# Run the App
# -------------------------------

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
