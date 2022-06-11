from flask import Blueprint
from flask_restx import Api

from namespaces.namespace_beacon import namespace_beacon

blueprint_ = Blueprint('user', __name__, url_prefix='/user')
api = Api(blueprint_user)
api.add_namespace(namespace_account, '/account')
