from flask_cors import CORS
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_extensions(app):
    CORS(app, resources={r"/*": {"origins": "*"}})