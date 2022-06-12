from flask import render_template, make_response
from flask_restx import Resource, Namespace, reqparse

from DB_handler.character_DB_handler import character_DB_handler
from DB_handler.movie_DB_handler import movie_DB_handler

namespace_movie = Namespace('movie', 'Api for movie')


@namespace_movie.route('/')
class GetAllCharacterData(Resource):
    def get(self):
        from flask import request
        movie_name = request.args.get("movie").replace(" ", "-")
        headers = {'Content-Type': 'text/html'}
        try:
            movie_list = movie_DB_handler.get_all_movies()
            character_list = character_DB_handler.get_all_characters(movie_name)
        except Exception as e:
            return str(e)
        return make_response(
            render_template("movie.html", movie_name_list=[movie.name.replace("-", " ") for movie in movie_list],
                            movie_name=movie_name.replace("-", " "), character_list=character_list))
