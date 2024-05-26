
from flask import Blueprint

app_views = Blueprint('views_blueprint',
                      __name__,
                      url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
