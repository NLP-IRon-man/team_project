from pathlib import Path

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from typing import List, Dict
from pandas import DataFrame
import pandas as pd
import os
import copy
from collections import OrderedDict
import matplotlib.pyplot as plt


def convert_dict_to_list(dictionary: Dict) -> List:
    return [data for _, data in sorted(
            dictionary.items(), key=lambda item: int(item[0]))]


def read_emotion_csv(dir_path: str) -> Dict:
    file_name_list = os.listdir(dir_path)
    raw_data_dict = {}
    for file_name in file_name_list:
        file_path = f"{dir_path}/{file_name}"
        data = pd.read_csv(file_path).to_dict()
        raw_data_dict[Path(file_name).with_suffix(
            "").name.replace("_emotion", "")] = data
    result_dict = {}
    for movie_name, movie_data in raw_data_dict.items():
        result_dict[movie_name] = {}
        character_name_list = convert_dict_to_list(movie_data["name"])
        character_name_list = list(OrderedDict.fromkeys(character_name_list))
        emotion_name_list = convert_dict_to_list(movie_data["Unnamed: 0"])
        emotion_name_list = list(OrderedDict.fromkeys(emotion_name_list))
        emotion_number = len(emotion_name_list)
        for period_name, period_data in movie_data.items():
            if period_name in ("name", "Unnamed: 0"):
                continue
            period_data = [data for _, data in sorted(
                period_data.items(), key=lambda item: int(item[0]))]
            splitted_by_character = [period_data[i:i+emotion_number]
                                     for i in range(0, len(period_data), emotion_number)]
            for character_idx, character_name in enumerate(character_name_list):
                if character_name not in result_dict[movie_name]:
                    result_dict[movie_name][character_name] = {}
                result_dict[movie_name][character_name][period_name] = {
                    emotion_name_list[emotion_idx]: splitted_by_character[character_idx][emotion_idx] for emotion_idx in range(emotion_number)}
    return result_dict


emotion_data_dict = read_emotion_csv("./code/emotion_csv")
movie_name = "Up"
character_name = "CARL"
period_name_list = list(emotion_data_dict[movie_name][character_name].keys())
print("..")
# period_name = "period_0"
# emotion_name = "disgust"
# plt.figure(figsize=(8, 8))
# plt.title(f"{movie_name} - {character_name}")
# for period_name in period_name_list:


# plt.scatter(x, y, color="blue")
# plt.axline((0, 0), slope=principal_component_1[1] /
#            principal_component_1[0], color="red", linestyle="-")
# plt.scatter(projection1[:, 0], projection1[:, 1], color="green")
# #
# # ++++++++++++++++++++++++++++++++++++++++++++++++++

# plt.xlim(min_x - 0.5, max_x + 0.5)
# plt.ylim(min_y - 0.5, max_y + 0.5)

# plt.tight_layout()
# plt.show()

# 사용자가 웹 사이트에서 imsdb 대본을 가져와서 해당 영화를 분석하고 싶다.
# 그 영화 대본 사이트 링크를 가져와서 html 웹 페이지에 입력한다.
# 서버. 로컬 (127.0.0.1) 콘솔로 해도 된다.
# 그 사이트에서 데이터를 크롤링해와서 일련의 과정을 수행한 후 결과를 보여준다.
