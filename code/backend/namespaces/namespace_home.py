from flask import render_template, make_response
from flask_restx import Resource, Namespace

from DB_handler.movie_DB_handler import movie_DB_handler

namespace_home = Namespace('home', 'Api for home')


@namespace_home.route('/')
class Index(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        movie_list = movie_DB_handler.get_all_movies()
        return make_response(render_template("index.html",
                                             movie_name_list=[movie.name.replace("-", " ") for movie in movie_list]))
