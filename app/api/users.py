from flask import request, jsonify
from app.api import bp
from app.api.errors import bad_request
import app.database as db_client

@bp.route('/users/signup', methods=['POST'])
def signup_user():
  form = request.form
  proposed_username = form['username']
  proposed_password = form['password']
  if proposed_username is None or proposed_password is None: 
    return bad_request('Must provide username and password.')

  ## optional TODO: add some checks on password to make sure it is strong

  # Confirm username is not taken
  existing_user = db_client.query_users_by_username(proposed_username).first()
  if existing_user is not None: 
    return bad_request('This username is taken.')

  # Add user into databse
  new_user = db_client.insert_user(proposed_username, proposed_password)

  response = jsonify({ 'userUid': new_user.id })
  response.statusCode = 201
  return response

@bp.route('/users/login', methods=['GET'])
def login_user():
  form = request.form
  username = form['username']
  password = form['password']
  if username is None or password is None: 
    return bad_request('Must provide username and password.')

  ## Confirm user exists
  existing_user = db_client.query_users_by_username(username).first()
  if existing_user is None: 
    return bad_request('No user found.')

  ## Confirm user provided correct password
  password_match = existing_user.check_password(password)
  if password_match is False:
    return bad_request('Incorrect password.')

  response = jsonify('Success')
  response.statusCode = 201
  return response