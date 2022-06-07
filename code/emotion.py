import os
preprocess_path = "./preprocess"
movies = os.listdir(preprocess_path)
import pandas as pd
from pandas import DataFrame
movie_name = "Joker" #영화제목
period_num = 5 #몇분할 할건지
print("processing.", end='')
for movie in movies:
    movie_path = './preprocess/'+movie
    movie_name = movie[:-15]

    period_emotion = []
    script = pd.read_csv(movie_path)
    emotion_df = pd.read_csv('emotion_dataset.csv')
    emotion_df = emotion_df.set_index('word')
    emotion = emotion_df.to_dict()
    emotion_list = ['disgust', 'surprise','neutral','anger','sad','happy','fear']

    disgust_dic = emotion['disgust']
    surprise_dic = emotion['surprise']
    neutral_dic = emotion['neutral']
    anger_dic = emotion['anger']
    sad_dic = emotion['sad']
    happy_dic = emotion['happy']
    fear_dic = emotion['fear']

    drop_unnamed = script.drop([script.columns[0]], axis = 1)
    test = drop_unnamed.rename(index={0: "text"})
    role = []
    for i in range(5):
        role.append(test.columns[i])
    dic = test.to_dict()

    for roles in role:
        txt_to_list = dic[roles]["text"].split(" ")
        length = len(txt_to_list)
        for i in range(period_num):
            count = 0
            tmp =[0,0,0,0,0,0,0]
            for j in range(i*(length//period_num),(i+1)*length//(period_num) - 1):
                if (txt_to_list[j]+" ") in disgust_dic:
                    count+=1
                    tmp[0] += disgust_dic[txt_to_list[j]+" "]
                    tmp[1] += surprise_dic[txt_to_list[j]+" "]
                    tmp[2] += neutral_dic[txt_to_list[j]+" "]
                    tmp[3] += anger_dic[txt_to_list[j]+" "]
                    tmp[4] += sad_dic[txt_to_list[j]+" "]
                    tmp[5] += happy_dic[txt_to_list[j]+" "]
                    tmp[6] += fear_dic[txt_to_list[j]+" "]
            #nparray = np.array(tmp)
            #nparray = nparray/count
            #period_emotion.append(nparray) #정규화를 위해서 해본건데 정규화가 아닌거같음 애당초 정규화가 필요한지 의문. 어차피 모든 단어마다 값이 다르니까
            period_emotion.append(tmp)

    data = {
        'name' : []
    }
    for i in range(period_num):
        data["period_"+str(i)] = []
    df = pd.DataFrame(data)

    for i in range(len(role)):
        new_data = {
            'name' : role[i]
        }
        for j in range(period_num):
            new_data["period_"+str(j)] = period_emotion[i*period_num+j]
        new_df = pd.DataFrame(new_data)
        df = df.append(new_df, ignore_index = True)

    index_list = emotion_list*len(role)
    df = df.set_index(keys=[index_list], inplace=False)
    movie[:-3]
    csv_name = movie_name + '_emotion.csv'
    path = './emotion_csv/'+csv_name
    df.to_csv(path)
    print(".", end='')
print()
