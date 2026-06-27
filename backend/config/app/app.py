from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", '..'))
FRONT_DIR = os.path.join(BASE_DIR, 'frontend', 'templates')

SECRET_KEY= os.getenv('SECRET_KEY')

app= Flask(__name__, template_folder=FRONT_DIR)
app.secret_key= SECRET_KEY
