from flask import Blueprint

blueprint = Blueprint('landing', __name__)

from . import views
