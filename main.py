from flask import Flask, request, send_file, jsonify
import uuid
import cv2 as cv
import requests
from flask_cors import CORS
from cv_helpers import test_fn

app = Flask('app')
CORS(app)

@app.route('/')
def hello_world():
  test_fn("test_fn input")
  return '<h1>Upload face image!</h1>'

@app.route('/upload-face-image',  methods=["POST"])
def upload_face_image():
  form_dict = request.form
  print("name: {}".format(form_dict["name"]))
  file_dict = request.files
  f = file_dict['faceImage']
  if f is None: 
    raise Exception('faceImage is null image.')
  uid = uuid.uuid1()
  print("uid: {}".format(uid))
  f.save('./face-image-uploads/{}.jpeg'.format(uid))

  img = cv.imread('./face-image-uploads/{}.jpeg'.format(uid))
  if img is None: 
    raise Exception('OpenCV read null image')
  rotated_img = cv.rotate(img, 0)
  cv.imwrite('./rotated-face-images/{}.jpeg'.format(uid), rotated_img)
  return jsonify({
    "uid": str(uid),
    "url": "https://flask-test.gundadittu.repl.co/get-rotated-face-  image/{}".format(uid)
  }), 200

@app.route('/get-rotated-face-image/<string:uid>', methods=['GET'])
def get_rotated_face_image(uid):
  return send_file('./rotated-face-images/{}.jpeg'.format(uid)), 200


@app.route('/test_http_requests', methods=['GET'])
def test_http_requests():
  r = requests.get('https://hacker-news.firebaseio.com/v0/item/8863.json')
  return r.json()

@app.errorhandler(Exception)
def handle_bad_request(e):
  print(e)
  return e, 500

app.run(host='0.0.0.0', port=8080)