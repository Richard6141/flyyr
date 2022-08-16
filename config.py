from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()
password=quote_plus(os.getenv('PASSWORD_DB'))
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:{}@localhost:5432/udacity'.format(password)
SQLALCHEMY_TRACK_MODIFICATIONS = False



# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:61413177@localhost:5432/udacity'
SQLALCHEMY_TRACK_MODIFICATIONS = False
