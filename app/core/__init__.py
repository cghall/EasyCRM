from flask import Blueprint

from models import Base, Contact, Organisation

core = Blueprint('core', __name__, template_folder='templates/core')

from . import controller
