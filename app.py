from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import requests
import uuid  

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

# -------------------------------
# Initialize Flask app
# -------------------------------
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'a8f3@9!gks92&x1z')  

# -------------------------------
# File Upload Config
# -------------------------------
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------------------
# Database configuration
# -------------------------------
database_url = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
if database_url.startswith("postgres://"):
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
    

    # --- Seed Pets Function ---

def seed_pets():
    if Pet.query.count() == 0:
        pets_available = [
            Pet(img='images/Golden-Retriever.png', name='Charlie', age=3, breed='Golden Retriever', species='Dog'),
            Pet(img='images/Beagle.png', name='Max', age=2, breed='Beagle', species='Dog'),
            Pet(img='images/Bulldogg.png', name='Rocky', age=5, breed='Bulldog', species='Dog'),
            Pet(img='images/Husky.png', name='Ghost', age=4, breed='Siberian Husky', species='Dog'),
            Pet(img='images/Tabby.png', name='Luna', age=1, breed='Tabby', species='Cat'),
            Pet(img='images/Siamese.png', name='Simba', age=3, breed='Siamese', species='Cat'),
            Pet(img='images/Persian.png', name='Nala', age=4, breed='Persian', species='Cat'),
            Pet(img='images/Bengal.png', name='Tiger', age=2, breed='Bengal', species='Cat'),
            Pet(img='images/Lop.png', name='Hazel', age=1, breed='Lop', species='Rabbit'),
            Pet(img='images/Rex.png', name='Cinnamon', age=2, breed='Rex', species='Rabbit'),
            Pet(img='images/Angora.png', name='Snowflake', age=2, breed='Angora', species='Rabbit'),
            Pet(img='images/Macaw.png', name='Skye', age=2, breed='Macaw', species='Bird'),
            Pet(img='images/Cockatiel.png', name='Sunny', age=1, breed='Cockatiel', species='Bird'),
            Pet(img='images/Parakeet.png', name='Kiwi', age=2, breed='Parakeet', species='Bird'),
            Pet(img='images/LeopardGecko.png', name='Leo', age=1, breed='Leopard Gecko', species='Reptile'),
            Pet(img='images/BeardedDragon.png', name='Spike', age=3, breed='Bearded Dragon', species='Reptile'),
            Pet(img='images/CornSnake.png', name='Slyther', age=2, breed='Corn Snake', species='Reptile'),
            Pet(img='images/BoxTurtle.png', name='Shelly', age=4, breed='Box Turtle', species='Reptile'),
            Pet(img='images/VeiledChameleon.png', name='Echo', age=2, breed='Veiled Chameleon', species='Reptile'),
        ]
        db.session.bulk_save_objects(pets_available)
        db.session.commit()

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
            "title": " Find your pet",
            "description": "Browse loving pets waiting for their forever home. Use our simple search to meet your perfect match and start your adoption journey today."
        },
        {
            "title": " Reach out to us",
            "description": "Got questions or ready to take the next step? Our friendly team is here to help with anything you need just a message or call away."
        },
        {
            "title": " Have A Meeting",
            "description": "Schedule a meet-and-greet to get to know your future furry friend. It’s the perfect way to see if it’s a match made in pawradise."
        }
    ]



    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'
        flash('Thank you for contacting us!!')
        return render_template('index.html', form_action=url_for('index'), first_name=first_name, surname=surname, email=email, message=message, terms=terms, steps=steps,)
    
    return render_template('index.html', steps=steps, form_action=url_for('index'))


# -------------------------------
# Pet listing page start
# -------------------------------

from sqlalchemy import distinct

@app.route('/pets', methods=['GET', 'POST'])
def list_pets():
    
    if Pet.query.count() == 0:
        pets_available = [
            Pet(img='images/Golden-Retriever.png', name='Charlie', age=3, breed='Golden Retriever', species='Dog'),
            Pet(img='images/Beagle.png', name='Max', age=2, breed='Beagle', species='Dog'),
            Pet(img='images/Bulldogg.png', name='Rocky', age=5, breed='Bulldog', species='Dog'),
            Pet(img='images/Husky.png', name='Ghost', age=4, breed='Siberian Husky', species='Dog'),
            Pet(img='images/Tabby.png', name='Luna', age=1, breed='Tabby', species='Cat'),
            Pet(img='images/Siamese.png', name='Simba', age=3, breed='Siamese', species='Cat'),
            Pet(img='images/Persian.png', name='Nala', age=4, breed='Persian', species='Cat'),
            Pet(img='images/Bengal.png', name='Tiger', age=2, breed='Bengal', species='Cat'),
            Pet(img='images/Lop.png', name='Hazel', age=1, breed='Lop', species='Rabbit'),
            Pet(img='images/Rex.png', name='Cinnamon', age=2, breed='Rex', species='Rabbit'),
            Pet(img='images/Angora.png', name='Snowflake', age=2, breed='Angora', species='Rabbit'),
            Pet(img='images/Macaw.png', name='Skye', age=2, breed='Macaw', species='Bird'),
            Pet(img='images/Cockatiel.png', name='Sunny', age=1, breed='Cockatiel', species='Bird'),
            Pet(img='images/Parakeet.png', name='Kiwi', age=2, breed='Parakeet', species='Bird'),
            Pet(img='images/LeopardGecko.png', name='Leo', age=1, breed='Leopard Gecko', species='Reptile'),
            Pet(img='images/BeardedDragon.png', name='Spike', age=3, breed='Bearded Dragon', species='Reptile'),
            Pet(img='images/CornSnake.png', name='Slyther', age=2, breed='Corn Snake', species='Reptile'),
            Pet(img='images/BoxTurtle.png', name='Shelly', age=4, breed='Box Turtle', species='Reptile'),
            Pet(img='images/VeiledChameleon.png', name='Echo', age=2, breed='Veiled Chameleon', species='Reptile'),
        ]
        db.session.bulk_save_objects(pets_available)
        db.session.commit()

    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')
        terms = request.form.get('terms') == 'on'
        flash('Thank you for contacting us!!')

        pets = Pet.query.all()
        species_options = [row[0] for row in db.session.query(distinct(Pet.species)).all()]
        return render_template(
            'pets.html',
            pets=pets,
            name='',
            age='',
            breed='',
            selected_species='',
            species_options=species_options,
            first_name=first_name,
            surname=surname,
            email=email,
            message=message,
            terms=terms,
        )

    
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

    return render_template(
        'pets.html',
        pets=pets,
        name=name,
        age=age,
        breed=breed,
        selected_species=species,
        species_options=species_options
    )


# -------------------------------
# Pet listing page end
# -------------------------------

# -------------------------------
# Add pet start
# -------------------------------


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            if 'image' not in request.files:
                flash("No image file part", "error")
                return redirect(request.url)

            file = request.files['image']

            if file.filename == '':
                flash("No image selected", "error")
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                img_path = f'uploads/{unique_filename}'
            else:
                flash("Allowed image types: png, jpg, jpeg, gif", "error")
                return redirect(request.url)

            name = request.form.get('name')
            age = request.form.get('age')
            breed = request.form.get('breed')
            species = request.form.get('species')

            if not name or not age or not breed or not species:
                flash("Please fill in all required fields!", "error")
                return redirect(request.url)

            try:
                age = int(age)
            except ValueError:
                flash("Age must be a number", "error")
                return redirect(request.url)

            new_pet = Pet(img=img_path, name=name, age=age, breed=breed, species=species)
            db.session.add(new_pet)
            db.session.commit()
            flash(f"Pet '{name}' added successfully!", "success")
            return redirect(url_for('list_pets'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(request.url)
    return render_template('add.html')


# -------------------------------
# Add pet end
# -------------------------------



# -------------------------------
# edit pets start 
# -------------------------------

@app.route('/edit/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)

    if request.method == 'POST':
        
        pet.name = request.form['name']
        pet.age = int(request.form['age'])
        pet.breed = request.form['breed']
        pet.species = request.form['species']

        
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                pet.img = filename
        
        db.session.commit()
        flash('Pet updated successfully!', 'success')
        return redirect(url_for('list_pets'))
    
    return render_template('edit.html', pet=pet)




@app.route('/delete_pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash(f"Deleted pet {pet.name}", "success")
    return redirect(url_for('list_pets'))

# -------------------------------
# edit pets end
# -------------------------------





# About page 
@app.route('/about', methods=['GET', 'POST'])
def about():
    sections = [
        {
            'image': "images/woman.png",
            'alt': 'woman and dog',
            'title': 'Our Mission',
            'paragraphs': [
                'At Pawfect, our mission is to ensure that every pet finds a loving and forever home.',
                'We believe in creating meaningful connections between caring people and animals in need, making the adoption process simple, safe, and joyful for everyone involved.'
            ],
            'reverse': False
        },
        {
            'image': "images/bulldog.png",
            'alt': 'woman and dog',
            'title': 'What We Do',
            'paragraphs': [
                'We provide a trusted platform where adopters can explore detailed profiles of pets looking for new families.',
                'Beyond just matching pets and people, we offer guidance, resources, and support throughout the entire adoption journey to help create lasting bonds.'
            ],
            'reverse': True
        },
        {
            'image': "images/man.png",
            'alt': 'woman and dog',
            'title': 'Our Promise',
            'paragraphs': [
                'We are committed to transparency, compassion, and the well-being of every animal in our care.',
                'Whether you’re adopting, volunteering, or simply learning more, Pawfect is dedicated to fostering a community where every paw finds the perfect place to call home.'
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
