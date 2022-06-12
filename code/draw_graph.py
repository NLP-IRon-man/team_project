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
import numpy as np
import unicodedata

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

def movie_list(dir_path: str) -> Dict:
    file_name_list = os.listdir(dir_path)
    result = []
    for item in file_name_list:
        result.append(item[:-12])
    return result


def convert_emotion_data_dict_to_graph_data_dict(emotion_data_dict: Dict) -> Dict:
    graph_data = {}
    for movie_name, movie_data in emotion_data_dict.items():
        graph_data[movie_name] = {}
        for character_name, character_data in movie_data.items():
            graph_data[movie_name][character_name] = {}
            for _, period_data in character_data.items():
                for emotion_name, emotion_data in period_data.items():
                    if emotion_name not in graph_data[movie_name][character_name]:
                        graph_data[movie_name][character_name][emotion_name] = []
                    graph_data[movie_name][character_name][emotion_name].append(
                        emotion_data)
    return graph_data


#emotion_data_dict = read_emotion_csv("./code/emotion_csv")
emotion_data_dict = read_emotion_csv("emotion_csv")
graph_data_dict = convert_emotion_data_dict_to_graph_data_dict(
    emotion_data_dict)
movies = movie_list("emotion_csv")
"""
for movie in movies:
    movie_name = movie
    for role in graph_data_dict[movie_name]:
        character_name = role

#movie_name = "Up"
#character_name = "CARL"
        period_name_list = [period_name.replace("_", " ").replace(
            "p", "P") for period_name in list(emotion_data_dict[movie_name][character_name].keys())]
        emotion_name_list = list(
            emotion_data_dict[movie_name][character_name]["period_0"].keys())
        print("..")
        # period_name = "period_0"
        # emotion_name = "disgust"
        graph_data = {}
        period_axis = np.arange(len(period_name_list))
        plt.figure(figsize=(8, 8))
        plt.title(f"{movie_name} - {character_name}")
        plt.xticks(period_axis, period_name_list)
        for emotion_idx, emotion_name in enumerate(emotion_name_list):
            plt.plot(
                period_axis, graph_data_dict[movie_name][character_name][emotion_name], label=emotion_name)
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.tight_layout()
        file_name = movie_name + "_" + role+".png"
        plt.savefig('plot_image/'+file_name)
#plt.show()

        for period_name in period_name_list:
            for emotion_name in emotion_name_list:
                print()
"""
print()
print("processing", end="")
for movie in movies:
    movie_name = movie
    for role in graph_data_dict[movie_name]:



        character_name = role
        period_name_list = [period_name.replace("_", " ").replace(
            "p", "P") for period_name in list(emotion_data_dict[movie_name][character_name].keys())]
        emotion_name_list = list(
            emotion_data_dict[movie_name][character_name]["period_0"].keys())
        print("..", end="")
        percent_dict = {'disgust':[], 'surprise':[], 'neutral':[], 'anger':[],'sad':[],'happy':[],'fear':[]}
        for i in range(len(period_name_list)):
            temp_sum = 0
            for emotion in emotion_name_list:
                temp_sum+=graph_data_dict[movie_name][character_name][emotion][i]
            for emotion in emotion_name_list:
                if graph_data_dict[movie_name][character_name][emotion][i]==0:
                    percent_dict[emotion].append(0)
                else:
                    percent_dict[emotion].append((graph_data_dict[movie_name][character_name][emotion][i]/temp_sum)*100)
        
        ##most emotion
        most_emotions = []
        most_values = []
        emoji_dict = {'happy': "😀",'fear': "😱",'disgust': "🤮",'surprise': "😲",'neutral': "😐",'anger': "😡",'sad': "😭"}
        for i in range(len(period_name_list)):
            max_emotion = ''
            temp = 0
            for emotion in emotion_name_list:
                if percent_dict[emotion][i]>=temp:
                    max_emotion = emotion
                    temp = percent_dict[emotion][i]
            most_emotions.append(max_emotion)
            most_values.append(temp)
        

        period_axis = np.arange(len(period_name_list))
        plt.figure(figsize=(8, 8))
        plt.title(f"{movie_name} - {character_name}")
        plt.xticks(period_axis, period_name_list)
        for emotion_idx, emotion_name in enumerate(emotion_name_list):
            plt.plot(
                period_axis, percent_dict[emotion_name], label=emotion_name)
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.tight_layout()
        for i in range(len(period_name_list)):
            plt.text(i-0.5,most_values[i],most_emotions[i]+emoji_dict[most_emotions[i]], fontsize=12, color='black', weight = 'bold')

        file_name = movie_name + "_" + role+".png"
        plt.savefig('plot_image/'+file_name)
#plt.show()
