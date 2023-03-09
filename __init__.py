import os

from flask import Flask
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
