from pathlib import Path

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from typing import List, Dict
from pandas import DataFrame
import pandas as pd
import os

scripts_path = "./scripts"
scripts_name = os.listdir(scripts_path)
movie_data_dict = {}
for script_name in scripts_name:
    csv_name = Path(script_name).with_suffix(".csv").name
    csv_path = './csv/' + csv_name
    movie_data = pd.read_csv(csv_path).to_dict()
    movie_data_dict[Path(script_name).with_suffix("")] = movie_data

movie_data_dict = {k: {k1: v1[0] for k1, v1 in v.items()} for k, v in movie_data_dict.items()}
for _, v in movie_data_dict.items():
    del (v["Unnamed: 0"])
stop_words = set(stopwords.words("english"))
tokenizer = nltk.RegexpTokenizer(r"\w+")
lemmatizer = WordNetLemmatizer()


def tokenize(sentence: str):
    return tokenizer.tokenize(sentence)


def lemmatize(token_list: List[str]):
    return [lemmatizer.lemmatize(t) for t in token_list]


def remove_stop_words(token_list: List[str]) -> List[str]:
    return [t for t in token_list if not t.lower() in stop_words]


def print_movie_data(movie_data_dict: Dict):
    for name, data in movie_data_dict.items():
        print(f"[{name}]")
        for character, line in data.items():
            print(f"\t/{character}/")
            print(f"\t{line}")


def process_data(movie_data_dict: Dict, fn):
    for name, data in movie_data_dict.items():
        for character, line in data.items():
            data[character] = fn(line)


process_data(movie_data_dict, tokenize)
print("\n**After tokenizing")
print_movie_data(movie_data_dict)

process_data(movie_data_dict, lemmatize)
print("\n**After lemmatizing")
print_movie_data(movie_data_dict)

process_data(movie_data_dict, remove_stop_words)
print("\n**After removing stop words")
print_movie_data(movie_data_dict)
