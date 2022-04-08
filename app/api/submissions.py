import cv2 as cv
from flask import request, jsonify
from app.api import bp
from app.api.auth import basic_auth
from app.api.errors import bad_request
import app.database as db_client

@bp.route('/submissions/create-submission', methods=['POST'])
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

  # Add user's submission into database
  submission = db_client.insert_submission(current_user_uid)
  submission_uid = submission.id

  # Save raw image to disk
  raw_img_file_path = '/submissions/raw/{}.jpeg'.format(submission_uid)
  f.save(raw_img_file_path)

  # Rotate image 90 degrees
  img = cv.imread(raw_img_file_path)
  rotated_img = cv.rotate(img, 0)

  ## TODO: add more computer vision annotations to image

  # Save rotated image to disk
  rotated_img_file_path = '/submissions/rotated/{}.jpeg'.format(submission_uid)
  cv.imwrite(rotated_img_file_path, rotated_img)

  ## TODO: save submission uid to user in database
  
  return jsonify({
    "submissionUid": str(submission_uid),
  }), 200


## TODO: create endpoint to get raw images for a submission
## TODO: create endpoint to get rotated images for a submissions
## TODO: create endpoint to get all submissions for user