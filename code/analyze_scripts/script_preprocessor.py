from pathlib import Path

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from typing import List, Dict
from pandas import DataFrame
import pandas as pd
import os
import copy


class ScriptPreprocessor:
    def __init__(self, main_character_figured_out_csv_base_path: str,
                 output_base_path: str):
        self.__main_character_figured_out_csv_base_path = main_character_figured_out_csv_base_path
        self.__output_base_path = output_base_path
        self.__main_character_figured_out_csv_list = os.listdir(self.__main_character_figured_out_csv_base_path)
        self.__movie_data_dict = {}
        self.__read_main_character_figured_out_csv()
        self.__stop_words = set(stopwords.words("english"))
        self.__tokenizer = nltk.RegexpTokenizer(r"\w+")
        self.__lemmatizer = WordNetLemmatizer()

    def __read_main_character_figured_out_csv(self):
        for csv_filename in self.__main_character_figured_out_csv_list:
            csv_path = f"{self.__main_character_figured_out_csv_base_path}{csv_filename}"
            self.__movie_data_dict[Path(csv_filename).with_suffix("").name] = pd.read_csv(csv_path).to_dict()

        self.__movie_data_dict = {k: {k1: v1[0] for k1, v1 in v.items()}
                                  for k, v in self.__movie_data_dict.items()}
        for _, v in self.__movie_data_dict.items():
            del (v["Unnamed: 0"])

    def __tokenize(self):
        for name, data in self.__movie_data_dict.items():
            for character, line in data.items():
                data[character] = self.__tokenizer.tokenize(line)

    def __lemmatize(self):
        for name, data in self.__movie_data_dict.items():
            for character, token_list in data.items():
                data[character] = [self.__lemmatizer.lemmatize(t) for t in token_list]

    def __remove_stop_words(self):
        for name, data in self.__movie_data_dict.items():
            for character, token_list in data.items():
                data[character] = [t for t in token_list if not t.lower() in self.__stop_words]

    def __print_movie_data(self):
        for name, data in self.__movie_data_dict.items():
            print(f"[{name}]")
            for character, line in data.items():
                print(f"\t/{character}/")
                print(f"\t{line}")

    def __save_data(self):
        copied_data_dict = copy.deepcopy(self.__movie_data_dict)
        for name, data in copied_data_dict.items():
            for character, token_list in data.items():
                data[character] = " ".join(token_list)
        for name, data in copied_data_dict.items():
            csv_path = f"{self.__output_base_path}{name}_preprocess.csv"
            DataFrame.from_dict([data]).to_csv(csv_path)

    @staticmethod
    def read_output_data(output_csv_path: str) -> Dict:
        return pd.read_csv(output_csv_path, index_col=0).to_dict()

    def run(self):
        self.__tokenize()
        self.__lemmatize()
        self.__remove_stop_words()
        self.__save_data()
