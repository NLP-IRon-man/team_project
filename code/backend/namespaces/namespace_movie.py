from flask import render_template, make_response
from flask_restx import Resource, Namespace, reqparse

from backend.handler.character_DB_handler import character_DB_handler

namespace_movie = Namespace('movie', 'Api for movie')


@namespace_movie.route('/<string:movie_name>/all')
class GetAllMovieCharacterData(Resource):
    def get(self, movie_name: str):
        try:
            character_list = character_DB_handler.get_all_characters(movie_name)
        except Exception as e:
            return str(e)
        for character in character_list:
            print(f"character: {character.name}")
        return render_template("movie.html")


@namespace_movie.route("/<string:movie_name>/<int:character_index>")
class GetMovieCharacterData(Resource):
    def get(self, movie_name: str, character_index: int):
        headers = {"Content-Type": "text/html"}
        try:
            character = character_DB_handler.get_character(movie_name, character_index)
        except Exception as e:
            return make_response(render_template("index.html", movie_name="joker", character_name="joker"))
            return str(e)
        print(f"character: {character.name}")
        return render_template("movie_character.html", movie_name="joker", character_name="joker")
