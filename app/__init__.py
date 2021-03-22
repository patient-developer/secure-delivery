from flask import Flask
from config import Config
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = Flask(__name__)
app.config.from_object(Config)

from app import routes
