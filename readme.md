# 🐾 Pawfect

**Pawfect** is a full-stack Flask web application that helps users explore adoptable pets and submit adoption inquiries. It features an editorial-style layout with a clean and engaging front-end, powered by a PostgreSQL database and deployed on Render.

🔗 **Live Site**: [https://pawfect-match-b7p8.onrender.com/]

## 🚀 Key Features

- 📋 **Pet Listings** – Browse all available pets with detailed profiles.
- ➕ **Add & Edit Pets** – Admin-style routes for adding and managing pet entries.
- 📨 **Contact Form** – Users can submit questions or adoption inquiries with feedback via flash messages.
- ❓ **FAQ & Questions Sections** – Informative content on the adoption process and common pet-related queries.
- 🐶 **Random Dog Facts** – Integrated with a public API to show new dog facts on each visit.
- 📊 **Adoption Stats** – Data-driven insights on adoption trends.
- 🧭 **Multi-Page Layout** – Includes Home, Pets, About, Contact, FAQ, and more.
- ⚡ **Dynamic UX** – Flash messaging for user feedback and clean navigation across pages.


## 🖥️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Deployment**: Render
- **API Integration**: Dog facts from [Dog API](https://dogapi.dog/api/v2/facts?)



## 📁 Project Structure

pawfect/

│
├── static/
│ ├── css/
│ └── images/
| └── Js/
│
│
├── templates/
│   ├── about.html
│   ├── add.html
│   ├── base.html             
│   ├── contact.html
│   ├── dog-fact.html         
│   ├── edit.html             
│   ├── faq.html
│   ├── featured-pets.html
│   ├── form.html             
│   ├── hero.html             
│   ├── how_we_work.html      
│   ├── index.html            
│   ├── pets.html             
│   ├── questions.html        
│   └── stats.html    
│
├── app.py
├── requirements.txt
└── README.md

## ✨ Requirements

alembic==1.16.4
blinker==1.9.0
click==8.2.1
Flask==3.1.1
Flask-Migrate==4.1.0
Flask-SQLAlchemy==3.1.1
greenlet==3.2.3
gunicorn==23.0.0
itsdangerous==2.2.0
Jinja2==3.1.6
Mako==1.3.10
MarkupSafe==3.0.2
packaging==25.0
psycopg2-binary==2.9.10
python-dotenv==1.1.1
requests==2.31.0
SQLAlchemy==2.0.41
typing_extensions==4.14.1
Werkzeug==3.1.3

