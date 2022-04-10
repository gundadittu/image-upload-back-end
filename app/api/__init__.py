from flask import Blueprint

"""
This file sets up the blueprint for api routes
Helpful doc: https://flask.palletsprojects.com/en/2.1.x/blueprints/
"""

bp = Blueprint('api', __name__)

from app.api import users, submissions, auth, errors