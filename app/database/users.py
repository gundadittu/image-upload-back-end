from app import db
from app.database.models import User

"""
This files defines all helper methods to access "Users" table in database
Helpful doc: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
"""

def query_users_by_username(username):
  return User.query.filter_by(username=username)

def insert_user(username, password):
  new_user = User()
  new_user.set_username(username)
  new_user.set_password(password)
  db.session.add(new_user)
  db.session.commit()
  return new_user