from typing import List

from DB_handler.DB_handler import DBHandler, DB_handler
from model.character import Character
from utility.utilities import make_error_message


class CharacterDBHandler:

    def __init__(self, _DB_handler: DBHandler):
        self.__DB_handler = _DB_handler

    def __connect_db(self):
        return self.__DB_handler.connect()

    def get_character(self, movie_name: str, character_index: int) -> Character:
        with self.__connect_db() as db:
            try:
                with db.cursor() as cursor:
                    sql = f"SELECT * FROM movie.characters " \
                          f"WHERE movie_name = '{movie_name}' AND id = '{character_index}';"
                    cursor.execute(sql)
                    character_info = cursor.fetchone()
                    if character_info is None or len(character_info) == 0:
                        raise Exception(
                            make_error_message(f"Character #{character_index} is not existed in movie '{movie_name}'"))
                    return Character(int(character_info[0]), character_info[1], character_info[2], character_info[3])
            except Exception as e:
                raise Exception(make_error_message(str(e)))

    def add_new_character(self, character: Character):
        with self.__connect_db() as db:
            try:
                with db.cursor() as cursor:
                    sql = f"INSERT INTO movie.characters (id, movie_name, name, " \
                          f"emotion_analysis_image_path) " \
                          f"VALUES('{character.index}', " \
                          f"'{character.movie_name}', " \
                          f"'{character.name}'," \
                          f"'{character.emotion_analysis_image_path}'); "
                    cursor.execute(sql)
                    db.commit()
                    return
            except Exception as e:
                raise Exception(make_error_message(str(e)))

    def get_all_characters(self, movie_name: str) -> List[Character]:
        with self.__connect_db() as db:
            try:
                with db.cursor() as cursor:
                    sql = f"SELECT * FROM movie.characters " \
                          f"WHERE movie_name = '{movie_name}';"
                    cursor.execute(sql)
                    character_info_list = cursor.fetchall()
                    if character_info_list is None or len(character_info_list) == 0:
                        raise Exception(make_error_message(f"There is no movie whose name is '{movie_name}'"))
                    character_list = [
                        Character(int(character_info[0]), character_info[1], character_info[2], character_info[3])
                        for character_info in character_info_list]
                    return character_list
            except Exception as e:
                raise Exception(make_error_message(str(e)))


character_DB_handler = CharacterDBHandler(DB_handler)
