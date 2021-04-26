from flask import Blueprint

blueprint = Blueprint('delivery', __name__)

from . import forms, views
