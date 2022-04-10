from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

"""
This file defines the application's models and associated database table structure.
Helpful doc: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
"""

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  submissions = db.relationship('Submission', backref='user', lazy=True)

  def set_username(self, username):
    self.username = username
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
      
  def __repr__(self):
    return '<User {}>'.format(self.username)

class Submission(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  title = db.Column(db.Text, nullable=False)
  
  def set_user_id(self, user_id):
    self.user_id = user_id

  def set_title(self, title):
    self.title = title

  def __repr__(self):
    return '<Submission {}>'.format(self.id)