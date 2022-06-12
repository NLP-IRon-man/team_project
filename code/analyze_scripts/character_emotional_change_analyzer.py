import os
import pandas as pd


class CharacterEmotionalChangeAnalyzer:
    def __init__(self, emotion_dataset_path: str, preprocessed_csv_base_path: str,
                 output_base_path: str, period_num: int):
        self.__emotion_dataset_path = emotion_dataset_path
        self.__preprocessed_csv_base_path = preprocessed_csv_base_path
        self.__movie_list = os.listdir(self.__preprocessed_csv_base_path)
        self.__output_base_path = output_base_path
        self.__period_num = period_num

    def run(self):
        print("processing.", end='')
        for movie in self.__movie_list:
            movie_path = self.__preprocessed_csv_base_path + movie
            movie_name = movie[:-15]

            period_emotion = []
            script = pd.read_csv(movie_path)
            emotion_df = pd.read_csv(self.__emotion_dataset_path)
            emotion_df = emotion_df.set_index('word')
            emotion = emotion_df.to_dict()
            emotion_list = ['disgust', 'surprise', 'neutral', 'anger', 'sad', 'happy', 'fear']

            disgust_dic = emotion['disgust']
            surprise_dic = emotion['surprise']
            neutral_dic = emotion['neutral']
            anger_dic = emotion['anger']
            sad_dic = emotion['sad']
            happy_dic = emotion['happy']
            fear_dic = emotion['fear']

            drop_unnamed = script.drop([script.columns[0]], axis=1)
            test = drop_unnamed.rename(index={0: "text"})
            role = []
            for i in range(5):
                role.append(test.columns[i])
            dic = test.to_dict()

            for roles in role:
                txt_to_list = dic[roles]["text"].split(" ")
                length = len(txt_to_list)
                for i in range(self.__period_num):
                    count = 0
                    tmp = [0, 0, 0, 0, 0, 0, 0]
                    for j in range(i * (length // self.__period_num), (i + 1) * length // self.__period_num - 1):
                        if (txt_to_list[j] + " ") in disgust_dic:
                            count += 1
                            if disgust_dic[txt_to_list[j] + " "] >= 0.007937:
                                tmp[0] += disgust_dic[txt_to_list[j] + " "]
                            if surprise_dic[txt_to_list[j] + " "] >= 0.026907:
                                tmp[1] += surprise_dic[txt_to_list[j] + " "]
                            if neutral_dic[txt_to_list[j] + " "] >= 0.003968:
                                tmp[2] += neutral_dic[txt_to_list[j] + " "]
                            if anger_dic[txt_to_list[j] + " "] >= 0.023810:
                                tmp[3] += anger_dic[txt_to_list[j] + " "]
                            if sad_dic[txt_to_list[j] + " "] >= 0.023810:
                                tmp[4] += sad_dic[txt_to_list[j] + " "]
                            if happy_dic[txt_to_list[j] + " "] >= 0.027778:
                                tmp[5] += happy_dic[txt_to_list[j] + " "]
                            if fear_dic[txt_to_list[j] + " "] >= 0.026316:
                                tmp[6] += fear_dic[txt_to_list[j] + " "]

                    period_emotion.append(tmp)

            data = {
                'name': []
            }
            for i in range(self.__period_num):
                data["period_" + str(i)] = []
            df = pd.DataFrame(data)

            for i in range(len(role)):
                new_data = {
                    'name': role[i]
                }
                for j in range(self.__period_num):
                    new_data["period_" + str(j)] = period_emotion[i * self.__period_num + j]
                new_df = pd.DataFrame(new_data)
                df = pd.concat([df, new_df], ignore_index=True)
                # df = df.append(new_df, ignore_index=True)

            index_list = emotion_list * len(role)
            df = df.set_index(keys=[index_list], inplace=False)
            movie[:-3]
            csv_name = movie_name + '_emotion.csv'
            path = self.__output_base_path + csv_name
            df.to_csv(path)
            print(".", end='')
        print()
