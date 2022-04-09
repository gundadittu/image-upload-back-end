from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  submissions = db.relationship('Submission', backref='user', lazy=True)
  ## TODO: add a field that holds list of submission ids

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

  def set_user_id(self, user_id):
    self.user_id = user_id

  def __repr__(self):
    return '<Submission {}>'.format(self.id)