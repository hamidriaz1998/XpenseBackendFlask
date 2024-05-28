from dotenv import load_dotenv
import os

load_dotenv()
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('CONNECTION_STRING')
