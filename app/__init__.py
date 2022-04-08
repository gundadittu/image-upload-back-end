from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
  app = Flask('app')
  app.config.from_object(Config)
  CORS(app)

  db.init_app(app)
  migrate.init_app(app, db)

  from app.api import bp as api_bp
  app.register_blueprint(api_bp, url_prefix='/api')
  
  return app

from app import models

# import uuid
# import cv2 as cv
# from flask import request, send_file, jsonify
## import requests

# @app.route('/')
# def home_page():
#   return '<h1>Upload image!</h1>'

## TODO: finish sign up
# @app.route('/sign-up')
# def sign_up():
#   form = request.form
#   proposed_username = form['username']
#   proposed_password = form['password']
#   if proposed_username is None or proposed_password is None: 
#     raise Exception('Must provide username and password.')

#   existing_user = query_users_by_username(proposed_username).first()
#   if existing_user is not None: 
#     raise Exception('This username is taken.')

#   insert_user(proposed_username, proposed_password)
#   return

# ## TODO: finish log in
# @app.route('/log-in')
# def log_in():
#   return

# ## TODO: need to save submission id to the user
# @app.route('/upload-raw-image',  methods=["POST"])
# def upload_raw_image():
#   # form_dict = request.form
#   file_dict = request.files
#   f = file_dict['rawImage']
#   if f is None: 
#     raise Exception('rawImage is null image.')
  
#   uid = uuid.uuid1()
#   print("uid: {}".format(uid))
  
#   f.save('./raw-image-uploads/{}.jpeg'.format(uid))

#   img = cv.imread('./raw-image-uploads/{}.jpeg'.format(uid))
#   if img is None: 
#     raise Exception('OpenCV read null image')
  
#   rotated_img = cv.rotate(img, 0)
#   cv.imwrite('./rotated-images/{}.jpeg'.format(uid), rotated_img)
  
#   return jsonify({
#     "uid": str(uid),
#     "url": "https://flask-test.gundadittu.repl.co/get-rotated-image/{}".format(uid)
#   }), 200

# @app.route('/get-rotated-image/<string:uid>', methods=['GET'])
# def get_rotated_image(uid):
#   return send_file('./rotated-images/{}.jpeg'.format(uid)), 200

# @app.errorhandler(Exception)
# def handle_bad_request(e):
#   print(e)
#   return e, 500

# app.run(host='0.0.0.0', port=8080)