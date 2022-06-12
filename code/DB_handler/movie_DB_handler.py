from DB_handler.DB_handler import DBHandler, DB_handler
from model.movie import Movie
from utility.utilities import make_error_message


class MovieDBHandler:

    def __init__(self, _DB_handler: DBHandler):
        self.__DB_handler = _DB_handler

    def __connect_db(self):
        return self.__DB_handler.connect()

    def get_all_movies(self):
        with self.__connect_db() as db:
            try:
                with db.cursor() as cursor:
                    sql = f"SELECT * FROM movie.movie;"
                    cursor.execute(sql)
                    movie_info_list = cursor.fetchall()
                    return [Movie(movie_info[0]) for movie_info in movie_info_list]
            except Exception as e:
                raise Exception(make_error_message(str(e)))

    def add_new_movie(self, movie: Movie):
        with self.__connect_db() as db:
            try:
                with db.cursor() as cursor:
                    sql = f"INSERT INTO movie.movie (name) " \
                          f"VALUES('{movie.name}'); "
                    cursor.execute(sql)
                    db.commit()
                    return
            except Exception as e:
                raise Exception(make_error_message(str(e)))


movie_DB_handler = MovieDBHandler(DB_handler)
