from pathlib import Path

from typing import List, Dict
import pandas as pd
import os
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
from DB_handler.movie_DB_handler import movie_DB_handler
from DB_handler.character_DB_handler import character_DB_handler
from model.character import Character
from model.movie import Movie
from distutils.dir_util import copy_tree


class GraphPlotter:
    def __init__(self, emotion_analyzed_csv_base_path: str,
                 output_graph_base_path: str, graph_base_path_for_web: str):
        self.__emotion_analyzed_csv_base_path: str = emotion_analyzed_csv_base_path
        self.__movie_list = []
        self.__get_movie_list()
        self.__emotion_analyzed_data_dict = {}
        self.__read_emotion_analyzed_data()
        self.__graph_data_dict = {}
        self.__convert_emotion_analyzed_data_to_graph_data()
        self.__output_graph_base_path = output_graph_base_path
        self.__graph_base_path_for_web = graph_base_path_for_web

    def __get_movie_list(self):
        file_name_list = os.listdir(self.__emotion_analyzed_csv_base_path)
        for item in file_name_list:
            self.__movie_list.append(item[:-12])

    def __read_emotion_analyzed_data(self):
        file_name_list = os.listdir(self.__emotion_analyzed_csv_base_path)
        raw_data_dict = {}
        for file_name in file_name_list:
            file_path = f"{self.__emotion_analyzed_csv_base_path}{file_name}"
            data = pd.read_csv(file_path).to_dict()
            raw_data_dict[Path(file_name).with_suffix(
                "").name.replace("_emotion", "")] = data
        self.__emotion_analyzed_data_dict = {}
        for movie_name, movie_data in raw_data_dict.items():
            self.__emotion_analyzed_data_dict[movie_name] = {}
            character_name_list = self.__convert_dict_to_list(movie_data["name"])
            character_name_list = list(OrderedDict.fromkeys(character_name_list))
            emotion_name_list = self.__convert_dict_to_list(movie_data["Unnamed: 0"])
            emotion_name_list = list(OrderedDict.fromkeys(emotion_name_list))
            emotion_number = len(emotion_name_list)
            for period_name, period_data in movie_data.items():
                if period_name in ("name", "Unnamed: 0"):
                    continue
                period_data = [data for _, data in sorted(
                    period_data.items(), key=lambda item: int(item[0]))]
                splitted_by_character = [period_data[i:i + emotion_number]
                                         for i in range(0, len(period_data), emotion_number)]
                for character_idx, character_name in enumerate(character_name_list):
                    if character_name not in self.__emotion_analyzed_data_dict[movie_name]:
                        self.__emotion_analyzed_data_dict[movie_name][character_name] = {}
                    self.__emotion_analyzed_data_dict[movie_name][character_name][period_name] = {
                        emotion_name_list[emotion_idx]: splitted_by_character[character_idx][emotion_idx] for
                        emotion_idx in
                        range(emotion_number)}

    def __convert_emotion_analyzed_data_to_graph_data(self):
        for movie_name, movie_data in self.__emotion_analyzed_data_dict.items():
            self.__graph_data_dict[movie_name] = {}
            for character_name, character_data in movie_data.items():
                self.__graph_data_dict[movie_name][character_name] = {}
                for _, period_data in character_data.items():
                    for emotion_name, emotion_data in period_data.items():
                        if emotion_name not in self.__graph_data_dict[movie_name][character_name]:
                            self.__graph_data_dict[movie_name][character_name][emotion_name] = []
                        self.__graph_data_dict[movie_name][character_name][emotion_name].append(
                            emotion_data)

    @staticmethod
    def __convert_dict_to_list(dictionary: Dict) -> List:
        return [data for _, data in sorted(
            dictionary.items(), key=lambda item: int(item[0]))]

    def copy_graph_folder_to_static_folder(self):
        copy_tree(self.__output_graph_base_path, self.__graph_base_path_for_web)

    def run(self):
        print()
        print("processing", end="")
        for movie in self.__movie_list:
            movie_name = movie
            character_index = 0
            try:
                movie_DB_handler.add_new_movie(Movie(movie_name))
            except Exception:
                pass
            for role in self.__graph_data_dict[movie_name]:
                character_name = role
                period_name_list = [period_name.replace("_", " ").replace(
                    "p", "P") for period_name in
                    list(self.__emotion_analyzed_data_dict[movie_name][character_name].keys())]
                emotion_name_list = list(
                    self.__emotion_analyzed_data_dict[movie_name][character_name]["period_0"].keys())
                print("..", end="")
                percent_dict = {'disgust': [], 'surprise': [], 'neutral': [], 'anger': [], 'sad': [], 'happy': [],
                                'fear': []}
                for i in range(len(period_name_list)):
                    temp_sum = 0
                    for emotion in emotion_name_list:
                        temp_sum += self.__graph_data_dict[movie_name][character_name][emotion][i]
                    for emotion in emotion_name_list:
                        if self.__graph_data_dict[movie_name][character_name][emotion][i] == 0:
                            percent_dict[emotion].append(0)
                        else:
                            percent_dict[emotion].append(
                                (self.__graph_data_dict[movie_name][character_name][emotion][i] / temp_sum) * 100)

                ##most emotion
                most_emotions = []
                most_values = []
                emoji_dict = {'happy': "😀", 'fear': "😱", 'disgust': "🤮", 'surprise': "😲", 'neutral': "😐",
                              'anger': "😡", 'sad': "😭"}
                for i in range(len(period_name_list)):
                    max_emotion = ''
                    temp = 0
                    for emotion in emotion_name_list:
                        if percent_dict[emotion][i] >= temp:
                            max_emotion = emotion
                            temp = percent_dict[emotion][i]
                    most_emotions.append(max_emotion)
                    most_values.append(temp)

                d_list = percent_dict["disgust"]
                su_list = percent_dict["surprise"]
                n_list = percent_dict["neutral"]
                a_list = percent_dict["anger"]
                sa_list = percent_dict["sad"]
                h_list = percent_dict["happy"]
                f_list = percent_dict["fear"]

                df = pd.DataFrame(index=[period_name_list],
                                  data={
                                      'disgust': d_list,
                                      'surprise': su_list,
                                      'neutral': n_list,
                                      'anger': a_list,
                                      'sad': sa_list,
                                      'happy': h_list,
                                      'fear': f_list}
                                  )
                ax = df.plot(figsize=(8, 8), kind="bar", stacked=True, rot=0)
                ax.legend(bbox_to_anchor=(0.95, 1.0), loc='upper left')
                ax.set_title(f"{movie_name} - {character_name}")
                file_name = movie_name + "_" + role.replace("'", "") + ".png"
                graph_path = self.__output_graph_base_path + file_name
                plt.savefig(graph_path)
                try:
                    character_DB_handler.add_new_character(
                        Character(character_index, movie_name, character_name.replace("'", ""), file_name))
                except Exception:
                    pass
                character_index += 1
