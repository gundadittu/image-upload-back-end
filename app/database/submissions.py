from app import db
from app.database.models import Submission

def get_submission(submission_id):
  return Submission.query.filter_by(id=submission_id)

def get_all_submissions_for_user(user_id):
  return Submission.query.filter_by(user_id=user_id)

def delete_submission(submission):
  db.session.delete(submission)
  db.session.commit()
  return

def insert_submission(user_id):
  new_submission = Submission()
  new_submission.set_user_id(user_id)
  db.session.add(new_submission)
  db.session.commit()
  return new_submission