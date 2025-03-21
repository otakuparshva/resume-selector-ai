from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Job(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(50))
    location = db.Column(db.String(50))
    created_by = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    id = db.Column(db.String, primary_key=True)
    job_id = db.Column(db.String, db.ForeignKey('job.id'), nullable=False)
    candidate_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    resume_text = db.Column(db.Text, nullable=False)
    match_score = db.Column(db.Integer)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)