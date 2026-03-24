from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Project(db.Model):
    __tablename__ = 'projects'
    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(100), nullable=False)
    description  = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200))
    live_url     = db.Column(db.String(300))
    github_url   = db.Column(db.String(300))
    image_url    = db.Column(db.String(300))
    order_num    = db.Column(db.Integer, default=0)
    is_active    = db.Column(db.Boolean, default=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def tech_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]


class Skill(db.Model):
    __tablename__ = 'skills'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    icon_class  = db.Column(db.String(80))
    order_num   = db.Column(db.Integer, default=0)


class Education(db.Model):
    __tablename__ = 'education'
    id          = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(150), nullable=False)
    degree      = db.Column(db.String(150))
    field       = db.Column(db.String(150))
    start_year  = db.Column(db.String(10))
    end_year    = db.Column(db.String(20))
    description = db.Column(db.Text)
    icon_class  = db.Column(db.String(80), default='fas fa-graduation-cap')
    order_num   = db.Column(db.Integer, default=0)


class Experience(db.Model):
    __tablename__ = 'experience'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(150), nullable=False)
    company     = db.Column(db.String(150))
    period      = db.Column(db.String(80))
    description = db.Column(db.Text)
    icon_class  = db.Column(db.String(80), default='fas fa-briefcase')
    order_num   = db.Column(db.Integer, default=0)


class Message(db.Model):
    __tablename__ = 'messages'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(150), nullable=False)
    subject    = db.Column(db.String(200), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    is_read    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
