from flask import Blueprint
from flask_restx import Api

from backend.namespaces.namespace_home import namespace_home
from backend.namespaces.namespace_movie import namespace_movie

blueprint_home = Blueprint('user', __name__, url_prefix='/home')
api = Api(blueprint_home)
api.add_namespace(namespace_home, '/')

blueprint_movie = Blueprint("movie", __name__, url_prefix="/movie")
api = Api(blueprint_movie)
api.add_namespace(namespace_movie, "/")
