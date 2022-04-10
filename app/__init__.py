from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

"""
This file defines the logic to set up the Flask app
"""

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

from app.database import models