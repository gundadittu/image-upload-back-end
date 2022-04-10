import cv2 as cv
from flask import request, jsonify, send_file
from app.api import bp
from app.api.auth import basic_auth
from app.api.errors import bad_request
from config import basedir
import app.database as db_client
import os

"""
This file contains all api routes related to submissions (images uploaded by users)
"""

@bp.route('/submissions/create', methods=['POST'])
@basic_auth.login_required()
def create_submission():
  # Verify user is logged in
  current_user = basic_auth.current_user()
  if current_user is None:
    return bad_request('Please log in to submit images.')
  current_user_uid = current_user.id
  
  # Extract image from request
  file_dict = request.files
  f = file_dict['image']
  if f is None: 
    return bad_request('Image missing from submission.')
  file_name = f.filename

  try:
    # Add user's submission into database
    submission = db_client.insert_submission(current_user_uid, file_name)
  
    # Save raw image to disk
    submission_uid = submission.id
    raw_img_file_path = os.path.join('./submissions', 'raw', '{}.jpeg'.format(submission_uid))
    f.save(raw_img_file_path)
  
    # Rotate image 90 degrees
    raw_img = cv.imread(raw_img_file_path)
    rotated_img = cv.rotate(raw_img, 0)

    # Save rotated image to disk
    rotated_img_file_path = os.path.join('./submissions', 'rotated','{}.jpeg'.format(submission_uid))
    cv.imwrite(rotated_img_file_path, rotated_img)
  
    ## Detect faces
    gray_img = cv.cvtColor(raw_img, cv.COLOR_BGR2GRAY)
    faceCascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
      gray_img,
      scaleFactor=1.3,
      minNeighbors=3,
      minSize=(30, 30)
    )
    ## Annotate faces on image
    face_img = raw_img.copy()
    for (x, y, w, h) in faces:
      cv.rectangle(face_img, (x, y), (x + w, y + h), (0, 255, 0), 4)

    # Save image with annotated faces to disk
    face_img_file_path = os.path.join('./submissions', 'faces','{}.jpeg'.format(submission_uid))
    cv.imwrite(face_img_file_path, face_img)
    
    return jsonify({ "submissionUid": str(submission_uid) }), 200
  except:
    db_client.delete_submission(submission)
    return bad_request("Something unexpected went wrong. Please try again.")

@bp.route('/submissions/raw-image/<int:submission_id>', methods=['GET'])
def get_raw_submission_image(submission_id):
  submission = db_client.get_submission(submission_id).first()
  if submission is None:
    return bad_request('Could not find submission.')
  return send_file(os.path.join(basedir, 'submissions', 'raw', '{}.jpeg'.format(submission_id))), 200

@bp.route('/submissions/rotated-image/<int:submission_id>', methods=['GET'])
def get_rotated_submission_image(submission_id):
  submission = db_client.get_submission(submission_id).first()
  if submission is None:
    return bad_request('Could not find submission.')
  return send_file(os.path.join(basedir, 'submissions', 'rotated', '{}.jpeg'.format(submission_id))), 200

@bp.route('/submissions/faces-image/<int:submission_id>', methods=['GET'])
def get_faces_submission_image(submission_id):
  submission = db_client.get_submission(submission_id).first()
  if submission is None:
    return bad_request('Could not find submission.')
  return send_file(os.path.join(basedir, 'submissions', 'faces', '{}.jpeg'.format(submission_id))), 200