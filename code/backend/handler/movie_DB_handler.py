from enum import Enum, auto

from backend.model.movie import Movie
from typing import List
from backend.handler.DB_handler import DBHandler, DB_handler
from backend.utility.utilities import make_error_message


class MovieDBHandler:

    def __init__(self, _DB_handler: DBHandler):
        self.__DB_handler = _DB_handler

    def __connect_db(self):
        return self.__DB_handler.connect()

    def get_all_movies(self):
        with self.__connect_db() as db:
            try:
                with db.cursor() as cursor:
                    sql = f"SELECT * FROM movie.movies;"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result
            except Exception as e:
                raise Exception(make_error_message(str(e)))


movie_DB_handler = MovieDBHandler(DB_handler)
