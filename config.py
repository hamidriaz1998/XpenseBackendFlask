import os

if os.getenv('FLASK_ENV') == 'development':
    from dotenv import load_dotenv
    load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('CONNECTION_STRING')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
