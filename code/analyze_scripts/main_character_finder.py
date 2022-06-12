import os


class MainCharacterFinder:
    def __init__(self, script_base_path: str, output_base_path: str):
        self.__script_base_path = script_base_path
        self.__movie_list = os.listdir(self.__script_base_path)
        self.__output_base_path = output_base_path

    def run(self):
        for movie in self.__movie_list:
            movie_path = self.__script_base_path + movie
            f = open(movie_path, 'r')
            scripts_line = []  # 한 등장인물의 대사마다 쪼개서 배열에 저장하기 위한 배열
            while True:
                line = f.readline()
                scripts_line.append(line)
                if not line: break
            scripts_by_role = {}  # 등장인물별 대사를 저장하기 위한 사전
            role_appearance = {}  # 등장한 횟수를 측정하기 위한 사전. 캐릭터 : 등장횟수
            for item in scripts_line:
                split_role_txt = item.split(' | ')  # role|txt 이므로 split
                if len(split_role_txt) < 2:  ## 파싱이 잘못된 것이겠지만 role |NULL 이런 경우가 존재해서 오류가 나서 그 부분 예외처리
                    continue
                role = split_role_txt[0]
                if role == '':  # ''는 어떻게 걸러낼 수가 없어서 임의로 하드코딩
                    continue
                txt = split_role_txt[1]

                if role in scripts_by_role:
                    scripts_by_role[role] += txt  # 역할별 대사 계속 append
                    role_appearance[role] += 1  # 등장 횟수 카운트
                else:
                    scripts_by_role[role] = txt
                    role_appearance[role] = 1

            sorted_dict = sorted(role_appearance.items(), key=lambda item: item[1], reverse=True)[:10]  # 상위 10명을 선정
            score_by_appearance = {}  ##등장횟수별로 1~10까지 스코어를 매긴다
            score = 10

            for i in range(10):
                score_by_appearance[sorted_dict[i][0]] = score
                score -= 1
            # print("대사를 자주 친 상위 10명\n",score_by_appearance)

            ##다른사람에게 언급당한 순위
            score_by_mentioned = {}
            for role, txt in scripts_by_role.items():
                for key in score_by_appearance.keys():
                    count = txt.count(key)  # 각 인물의 대사마다 몇번 언급됐는지 카운트
                    if key in score_by_mentioned:
                        score_by_mentioned[key] += count
                    else:
                        score_by_mentioned[key] = count
            sorted_dict = sorted(score_by_mentioned.items(), key=lambda item: item[1], reverse=True)[:10]
            score_by_mentioned = {}
            score = 10
            for i in range(10):
                score_by_mentioned[sorted_dict[i][0]] = score
                score -= 1
            # print("다른사람에게 자주 언급당한 상위 10명\n",score_by_mentioned)

            score_sum = {}
            for key in score_by_mentioned.keys():
                score_sum[key] = score_by_mentioned[key] + score_by_appearance[key]
            result = sorted(score_sum.items(), key=lambda item: item[1], reverse=True)[:5]
            top_5_role = []
            for i in range(5):
                top_5_role.append(result[i][0])

            # 최종 결과를 role:대사 형태로 csv파일로 output
            raw_data = {}
            for role in top_5_role:
                raw_data[role] = scripts_by_role[role]
            f.close()

            import pandas as pd
            from pandas import DataFrame

            csv_name = movie[:-4] + '.csv'
            path = self.__output_base_path + csv_name
            data = DataFrame(raw_data, index=['txt'])
            data.to_csv(path)
            print('.', end='')
