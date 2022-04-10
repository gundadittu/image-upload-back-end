from app import db
from app.database.models import Submission

"""
This files defines all helper methods to access "Submissions" table in database
Helpful doc: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
"""

def get_submission(submission_id):
  return Submission.query.filter_by(id=submission_id)

def get_all_submissions_for_user(user_id):
  return Submission.query.filter_by(user_id=user_id).order_by(Submission.submitted_at.desc())

def delete_submission(submission):
  db.session.delete(submission)
  db.session.commit()
  return

def insert_submission(user_id, title):
  new_submission = Submission()
  new_submission.set_user_id(user_id)
  new_submission.set_title(title)
  db.session.add(new_submission)
  db.session.commit()
  return new_submission