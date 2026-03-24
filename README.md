# Ingabire Kalinda Irene – Personal Portfolio Website

A full-stack personal portfolio website built with **HTML, CSS, Bootstrap, JavaScript** (frontend) and **Python Flask + SQLite** (backend).

---

## Project Structure

```
portfolio_backend/
│
├── app.py                  # Main Flask application & all routes
├── database.py             # SQLAlchemy models (Project, Skill, Education, Experience, Message, AdminUser)
├── requirements.txt        # Python dependencies
│
├── templates/
│   ├── index.html          # Public portfolio page (Jinja2)
│   └── admin/
│       ├── base.html       # Admin layout with sidebar
│       ├── login.html      # Admin login page
│       ├── dashboard.html  # Admin dashboard with stats
│       ├── projects.html   # Projects list
│       ├── project_form.html
│       ├── skills.html     # Skills list
│       ├── skill_form.html
│       ├── education.html
│       ├── education_form.html
│       ├── experience.html
│       ├── experience_form.html
│       ├── messages.html   # Contact messages inbox
│       └── message_detail.html
│
├── static/
│   ├── css/
│   │   └── style.css       # Your existing stylesheet (copy here)
│   ├── js/
│   │   └── script.js       # Updated JS (Flask contact form)
│   └── images/
│       ├── profile1.jpg    # Your profile photo
│       ├── project1.png    # Elle Steps screenshot
│       ├── project2.png    # Eco-Streams screenshot
│       └── project3.png    # Women's Fashion Shop screenshot
│
└── instance/
    └── portfolio.db        # SQLite database (auto-created on first run)
```

---

## Technologies Used

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | HTML5, CSS3, Bootstrap 5, JavaScript |
| Backend    | Python 3, Flask 3                 |
| Database   | SQLite (via Flask-SQLAlchemy)     |
| Auth       | Session-based with hashed passwords (Werkzeug) |
| Icons      | Font Awesome 6                    |
| Version Control | Git & GitHub                |

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Copy your static files

Copy your existing frontend files into the correct folders:

```
static/css/style.css         ← your style.css
static/images/profile1.jpg   ← your profile photo
static/images/project1.png   ← project screenshots
static/images/project2.png
static/images/project3.png
static/INGABIRE_KALINDA_IRENE_CV.pdf  ← your CV
```

### 5. Run the application

```bash
python app.py
```

The app will:
- Automatically create the SQLite database (`instance/portfolio.db`)
- Seed it with your real data (projects, skills, education, experience)
- Start the development server at `http://127.0.0.1:5000`

---

## Admin Panel

Access the admin dashboard at:

```
http://127.0.0.1:5000/admin
```

**Default login credentials:**

| Field    | Value      |
|----------|------------|
| Username | `irene`    |
| Password | `admin123` |

> **Important:** Change the password after your first login by editing `seed_database()` in `app.py`.

### What you can do in the Admin Panel

- **Dashboard** – overview of all content + recent messages
- **Projects** – add, edit, delete, show/hide projects
- **Skills** – manage your technical skills list
- **Education** – update your academic qualifications
- **Experience** – manage internships and training
- **Messages** – read and reply to contact form submissions

---

## Contact Form

The contact form on the portfolio page sends messages directly to the database. No third-party service (like Formspree) is needed. All messages are stored in the `messages` table and can be read in the admin panel under **Messages**.

---

## Database Tables

| Table        | Description                          |
|--------------|--------------------------------------|
| `projects`   | Portfolio projects                   |
| `skills`     | Technical skills                     |
| `education`  | Education & certifications           |
| `experience` | Work, internship & training history  |
| `messages`   | Contact form submissions             |
| `admin_users`| Admin login credentials              |

---

## GitHub Version Control

Suggested commit workflow:

```bash
# Initial setup
git init
git add .
git commit -m "Initial project setup – Flask backend structure"

# As you work
git add .
git commit -m "Add admin dashboard with stats"
git commit -m "Connect contact form to SQLite database"
git commit -m "Add seed data for projects and skills"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## Deployment Notes (Optional)

To deploy on a live server (e.g. PythonAnywhere or Render):

1. Change `SECRET_KEY` in `app.py` to a long random string
2. Set `debug=False` in `app.py`
3. Use environment variables for sensitive config

---

## Author

**Ingabire Kalinda Irene**  
Software Developer Student | BTEC IT Level 3 Extended Diploma  
📍 Kigali, Rwanda  
📧 ingabirekalindairene@gmail.com  
🔗 [GitHub](https://github.com/ingabirekalindairene-crypto)

---

© 2026 Ingabire Kalinda Irene. All rights reserved.
