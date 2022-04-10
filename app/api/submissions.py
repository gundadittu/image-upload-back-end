import cv2 as cv
from flask import request, jsonify, send_file
from app.api import bp
from app.api.auth import basic_auth
from app.api.errors import bad_request
from config import basedir
import app.database as db_client
import os

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
  
  # Add user's submission into database
  submission = db_client.insert_submission(current_user_uid, file_name)

  try:
    # Save raw image to disk
    submission_uid = submission.id
    raw_img_file_path = os.path.join('./submissions', 'raw', '{}.jpeg'.format(submission_uid))
    f.save(raw_img_file_path)
  
    # Rotate image 90 degrees
    img = cv.imread(raw_img_file_path)
    rotated_img = cv.rotate(img, 0)
  
    ## TODO: add more computer vision annotations to image
  
    # Save rotated image to disk
    rotated_img_file_path = os.path.join('./submissions', 'rotated','{}.jpeg'.format(submission_uid))
    cv.imwrite(rotated_img_file_path, rotated_img)
      
    return jsonify({
      "submissionUid": str(submission_uid),
    }), 200
  except:
    db_client.delete_submission(submission)
    return bad_request("Something unexpected went wrong. Please try again.")
    

@bp.route('/submissions/raw-image/<int:submission_id>', methods=['GET'])
# @basic_auth.login_required()
def get_raw_submission_image(submission_id):
  # Verify user is logged in
  # current_user = basic_auth.current_user()
  # if current_user is None:
  #   return bad_request('Please log in to view image.')
  # current_user_uid = current_user.id

  # Extract submission from database
  submission = db_client.get_submission(submission_id).first()
  if submission is None:
    return bad_request('Could not find submission.')

  # Verify user permissions
  # submission_user_id = submission.user_id
  # if submission_user_id != current_user_uid:
  #   return bad_request('User does not have permission to view this submission.')
  
  return send_file(os.path.join(basedir, 'submissions', 'raw', '{}.jpeg'.format(submission_id))), 200

@bp.route('/submissions/rotated-image/<int:submission_id>', methods=['GET'])
# @basic_auth.login_required()
def get_rotated_submission_image(submission_id):
  # Verify user is logged in
  # current_user = basic_auth.current_user()
  # if current_user is None:
  #   return bad_request('Please log in to view image.')
  # current_user_uid = current_user.id

  # Extract submission from database
  submission = db_client.get_submission(submission_id).first()
  if submission is None:
    return bad_request('Could not find submission.')

  # Verify user permissions
  # submission_user_id = submission.user_id
  # if submission_user_id != current_user_uid:
  #   return bad_request('User does not have permission to view this submission.')

  return send_file(os.path.join(basedir, 'submissions', 'rotated', '{}.jpeg'.format(submission_id))), 200