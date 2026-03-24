from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from database import db, Project, Skill, Education, Experience, Message, AdminUser
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'irene-portfolio-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')

db.init_app(app)

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin panel.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


# ─────────────────────────────────────────
#  PUBLIC PORTFOLIO ROUTES
# ─────────────────────────────────────────
@app.route('/')
def index():
    projects    = Project.query.filter_by(is_active=True).order_by(Project.order_num).all()
    skills      = Skill.query.order_by(Skill.order_num).all()
    education   = Education.query.order_by(Education.order_num).all()
    experiences = Experience.query.order_by(Experience.order_num).all()
    return render_template('index.html',
                           projects=projects,
                           skills=skills,
                           education=education,
                           experiences=experiences)


@app.route('/contact', methods=['POST'])
def contact():
    name    = request.form.get('name', '').strip()
    email   = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    if not all([name, email, subject, message]):
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    msg = Message(name=name, email=email, subject=subject, message=message)
    db.session.add(msg)
    db.session.commit()
    return jsonify({'success': True,
                    'message': 'Thank you! Your message has been saved. I will get back to you soon!'})


# ─────────────────────────────────────────
#  ADMIN – AUTH
# ─────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        admin    = AdminUser.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username']  = username
            flash('Welcome back, Irene!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password.', 'danger')

    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))


# ─────────────────────────────────────────
#  ADMIN – DASHBOARD
# ─────────────────────────────────────────
@app.route('/admin')
@admin_required
def admin_dashboard():
    stats = {
        'projects'   : Project.query.count(),
        'skills'     : Skill.query.count(),
        'education'  : Education.query.count(),
        'experiences': Experience.query.count(),
        'messages'   : Message.query.count(),
        'unread'     : Message.query.filter_by(is_read=False).count(),
    }
    recent_messages = Message.query.order_by(Message.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_messages=recent_messages)


# ─────────────────────────────────────────
#  ADMIN – PROJECTS
# ─────────────────────────────────────────
@app.route('/admin/projects')
@admin_required
def admin_projects():
    projects = Project.query.order_by(Project.order_num).all()
    return render_template('admin/projects.html', projects=projects)


@app.route('/admin/projects/add', methods=['GET', 'POST'])
@admin_required
def admin_add_project():
    if request.method == 'POST':
        project = Project(
            title       = request.form['title'],
            description = request.form['description'],
            technologies= request.form['technologies'],
            live_url    = request.form.get('live_url', ''),
            github_url  = request.form.get('github_url', ''),
            image_url   = request.form.get('image_url', ''),
            order_num   = int(request.form.get('order_num', 0)),
            is_active   = bool(request.form.get('is_active'))
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin_projects'))
    return render_template('admin/project_form.html', project=None, action='Add')


@app.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.title        = request.form['title']
        project.description  = request.form['description']
        project.technologies = request.form['technologies']
        project.live_url     = request.form.get('live_url', '')
        project.github_url   = request.form.get('github_url', '')
        project.image_url    = request.form.get('image_url', '')
        project.order_num    = int(request.form.get('order_num', 0))
        project.is_active    = bool(request.form.get('is_active'))
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin_projects'))
    return render_template('admin/project_form.html', project=project, action='Edit')


@app.route('/admin/projects/delete/<int:id>', methods=['POST'])
@admin_required
def admin_delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.', 'info')
    return redirect(url_for('admin_projects'))


# ─────────────────────────────────────────
#  ADMIN – SKILLS
# ─────────────────────────────────────────
@app.route('/admin/skills')
@admin_required
def admin_skills():
    skills = Skill.query.order_by(Skill.order_num).all()
    return render_template('admin/skills.html', skills=skills)


@app.route('/admin/skills/add', methods=['GET', 'POST'])
@admin_required
def admin_add_skill():
    if request.method == 'POST':
        skill = Skill(
            name        = request.form['name'],
            description = request.form['description'],
            icon_class  = request.form.get('icon_class', ''),
            order_num   = int(request.form.get('order_num', 0))
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added!', 'success')
        return redirect(url_for('admin_skills'))
    return render_template('admin/skill_form.html', skill=None, action='Add')


@app.route('/admin/skills/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_skill(id):
    skill = Skill.query.get_or_404(id)
    if request.method == 'POST':
        skill.name        = request.form['name']
        skill.description = request.form['description']
        skill.icon_class  = request.form.get('icon_class', '')
        skill.order_num   = int(request.form.get('order_num', 0))
        db.session.commit()
        flash('Skill updated!', 'success')
        return redirect(url_for('admin_skills'))
    return render_template('admin/skill_form.html', skill=skill, action='Edit')


@app.route('/admin/skills/delete/<int:id>', methods=['POST'])
@admin_required
def admin_delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted.', 'info')
    return redirect(url_for('admin_skills'))


# ─────────────────────────────────────────
#  ADMIN – EDUCATION
# ─────────────────────────────────────────
@app.route('/admin/education')
@admin_required
def admin_education():
    items = Education.query.order_by(Education.order_num).all()
    return render_template('admin/education.html', items=items)


@app.route('/admin/education/add', methods=['GET', 'POST'])
@admin_required
def admin_add_education():
    if request.method == 'POST':
        item = Education(
            institution = request.form['institution'],
            degree      = request.form['degree'],
            field       = request.form.get('field', ''),
            start_year  = request.form.get('start_year', ''),
            end_year    = request.form.get('end_year', ''),
            description = request.form.get('description', ''),
            icon_class  = request.form.get('icon_class', 'fas fa-graduation-cap'),
            order_num   = int(request.form.get('order_num', 0))
        )
        db.session.add(item)
        db.session.commit()
        flash('Education entry added!', 'success')
        return redirect(url_for('admin_education'))
    return render_template('admin/education_form.html', item=None, action='Add')


@app.route('/admin/education/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_education(id):
    item = Education.query.get_or_404(id)
    if request.method == 'POST':
        item.institution = request.form['institution']
        item.degree      = request.form['degree']
        item.field       = request.form.get('field', '')
        item.start_year  = request.form.get('start_year', '')
        item.end_year    = request.form.get('end_year', '')
        item.description = request.form.get('description', '')
        item.icon_class  = request.form.get('icon_class', 'fas fa-graduation-cap')
        item.order_num   = int(request.form.get('order_num', 0))
        db.session.commit()
        flash('Education entry updated!', 'success')
        return redirect(url_for('admin_education'))
    return render_template('admin/education_form.html', item=item, action='Edit')


@app.route('/admin/education/delete/<int:id>', methods=['POST'])
@admin_required
def admin_delete_education(id):
    item = Education.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Education entry deleted.', 'info')
    return redirect(url_for('admin_education'))


# ─────────────────────────────────────────
#  ADMIN – EXPERIENCE
# ─────────────────────────────────────────
@app.route('/admin/experience')
@admin_required
def admin_experience():
    items = Experience.query.order_by(Experience.order_num).all()
    return render_template('admin/experience.html', items=items)


@app.route('/admin/experience/add', methods=['GET', 'POST'])
@admin_required
def admin_add_experience():
    if request.method == 'POST':
        item = Experience(
            title       = request.form['title'],
            company     = request.form.get('company', ''),
            period      = request.form.get('period', ''),
            description = request.form.get('description', ''),
            icon_class  = request.form.get('icon_class', 'fas fa-briefcase'),
            order_num   = int(request.form.get('order_num', 0))
        )
        db.session.add(item)
        db.session.commit()
        flash('Experience entry added!', 'success')
        return redirect(url_for('admin_experience'))
    return render_template('admin/experience_form.html', item=None, action='Add')


@app.route('/admin/experience/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_experience(id):
    item = Experience.query.get_or_404(id)
    if request.method == 'POST':
        item.title       = request.form['title']
        item.company     = request.form.get('company', '')
        item.period      = request.form.get('period', '')
        item.description = request.form.get('description', '')
        item.icon_class  = request.form.get('icon_class', 'fas fa-briefcase')
        item.order_num   = int(request.form.get('order_num', 0))
        db.session.commit()
        flash('Experience entry updated!', 'success')
        return redirect(url_for('admin_experience'))
    return render_template('admin/experience_form.html', item=item, action='Edit')


@app.route('/admin/experience/delete/<int:id>', methods=['POST'])
@admin_required
def admin_delete_experience(id):
    item = Experience.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Experience entry deleted.', 'info')
    return redirect(url_for('admin_experience'))


# ─────────────────────────────────────────
#  ADMIN – MESSAGES
# ─────────────────────────────────────────
@app.route('/admin/messages')
@admin_required
def admin_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)


@app.route('/admin/messages/<int:id>')
@admin_required
def admin_view_message(id):
    msg = Message.query.get_or_404(id)
    if not msg.is_read:
        msg.is_read = True
        db.session.commit()
    return render_template('admin/message_detail.html', msg=msg)


@app.route('/admin/messages/delete/<int:id>', methods=['POST'])
@admin_required
def admin_delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted.', 'info')
    return redirect(url_for('admin_messages'))


# ─────────────────────────────────────────
#  INIT DB + SEED
# ─────────────────────────────────────────
def seed_database():
    """Populate with Irene's real data on first run."""
    if Project.query.first():
        return  # already seeded

    # Admin user
    admin = AdminUser(username='irene')
    admin.set_password('admin123')
    db.session.add(admin)

    # Skills
    skills_data = [
        ('HTML5',          'Semantic markup and structure',        'fab fa-html5',      1),
        ('CSS3',           'Responsive design & animations',       'fab fa-css3-alt',   2),
        ('JavaScript',     'DOM manipulation & interactivity',     'fab fa-js-square',  3),
        ('Python',         'Backend development & scripting',      'fab fa-python',     4),
        ('Bootstrap',      'Responsive frameworks',                'fab fa-bootstrap',  5),
        ('Databases',      'SQL & data management',                'fas fa-database',   6),
        ('Git & GitHub',   'Version control',                      'fab fa-git-alt',    7),
        ('Web Development','Full-stack development',               'fas fa-code',       8),
    ]
    for name, desc, icon, order in skills_data:
        db.session.add(Skill(name=name, description=desc, icon_class=icon, order_num=order))

    # Projects
    projects_data = [
        ('Elle Steps',
         'A responsive e-commerce website for a premium ladies\' footwear store with modern UI design.',
         'HTML5, CSS3, Responsive Design',
         'https://ingabirekalindairene-crypto.github.io/Elle-steps/', '', 'project1.png', 1),
        ('Eco-Streams Logistics',
         'A logistics and delivery platform focused on efficiency and eco-friendly transport solutions.',
         'HTML5, CSS3, JavaScript',
         'https://ingabirekalindairene-crypto.github.io/eco-stream-logistics/', '', 'project2.png', 2),
        ('Women\'s Fashion Shop',
         'An online fashion store showcasing trendy outfits with a clean and user-friendly interface.',
         'HTML5, CSS3, Responsive Design',
         'https://ingabirekalindairene-crypto.github.io/womens-fashion-shop/', '', 'project3.png', 3),
    ]
    for title, desc, tech, live, github, img, order in projects_data:
        db.session.add(Project(title=title, description=desc, technologies=tech,
                               live_url=live, github_url=github, image_url=img,
                               order_num=order, is_active=True))

    # Education
    db.session.add(Education(
        institution = 'BTEC IT Level 3 Extended Diploma',
        degree      = 'Extended Diploma',
        field       = 'Information and Technology',
        start_year  = '2024',
        end_year    = 'Present',
        description = 'Comprehensive diploma covering programming, database management, web development, and IT professional practices.',
        icon_class  = 'fas fa-graduation-cap',
        order_num   = 1
    ))

    # Experience
    experiences_data = [
        ('Academic Projects & Self-Learning',
         'BTEC IT Programme',
         'Ongoing',
         'Working on various projects as part of my BTEC IT diploma, including web development, software design, and database implementation.',
         'fas fa-briefcase', 1),
        ('Web Development Training',
         'Self-directed',
         'Current Focus',
         'Specializing in frontend and backend web development technologies. Building real-world projects to solidify understanding of HTML, CSS, JavaScript, Python, and databases.',
         'fas fa-code', 2),
        ('Internship – Software Developer',
         'Company / Organisation',
         '2026 – Present',
         'Working on a full-stack personal portfolio project as part of internship assignment, applying frontend and backend development skills.',
         'fas fa-laptop-code', 3),
    ]
    for title, company, period, desc, icon, order in experiences_data:
        db.session.add(Experience(title=title, company=company, period=period,
                                  description=desc, icon_class=icon, order_num=order))

    db.session.commit()
    print("✅ Database seeded with Irene's data.")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True)
