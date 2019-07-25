
"""Set Flask configuration vars."""

# General Config
SECRET_KEY = "OMG-SUPER-SECRET-yawoeN"
FLASK_APP = "run.py"

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///webapi.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
