from flask import render_template
from flask_restx import Resource, Namespace

namespace_home = Namespace('home', 'Api for home')


@namespace_home.route('/index')
class Index(Resource):
    def get(self):
        print("Index")
        return render_template("index.html")
