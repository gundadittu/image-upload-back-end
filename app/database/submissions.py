from app import db
from app.models import Submission

def insert_submission(user_id):
  new_submission = Submission()
  new_submission.set_user_id(user_id)
  db.session.add(new_submission)
  db.session.commit()
  return new_submission