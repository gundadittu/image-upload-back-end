from flask_httpauth import HTTPBasicAuth
from app.database.models import User
from app.api.errors import error_response

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    else:
      return None

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)