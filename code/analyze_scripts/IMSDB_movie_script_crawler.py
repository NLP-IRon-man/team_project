import os
from bs4 import BeautifulSoup
import urllib3
from utility.utilities import *
import certifi
import ssl


class IMSDBMovieScriptCrawler:
    def __init__(self, script_path: str):
        self.__script_path = script_path
        self.__movie_name: str = ""
        self.__url: str = ""
        self.__script: str = ""
        try:
            os.makedirs(self.__script_path)
        except:
            print(make_error_message('Folder already exists.'))

    def __make_script_url(self, movie_name: str):
        self.__movie_name = movie_name
        base_url = 'https://imsdb.com/scripts/'
        self.__url = f"{base_url}{self.__movie_name.replace(' ', '-')}.html"

    def run(self, movie_name: str):
        self.__make_script_url(movie_name)
        http = urllib3.PoolManager()
        response = http.request('GET', self.__url)
        soup = BeautifulSoup(response.data, "html.parser")

        save_path = os.path.dirname(os.path.abspath(
            __file__)) + '/scripts'
        file_name = self.__movie_name + '.txt'
        complete_name = os.path.join(save_path, file_name)

        count = 0

        print(self.__movie_name)
        script_file = open(complete_name, "w")

        charactor = ''
        script = ''

        script_dict = dict()
        # pre 라는 id를 통해 스크립트 내용을 iterator로 가져온다.
        # <b> 태그 -> <b> 태그 내용 -> 그 다음 script text 가 순서대로 나온다
        # ----------example-----------
        # count = 0 : <b> FATHER </b>
        # count = 1 :     FATHER
        # count = 2 : Yes, my son?
        for element in soup.find('pre').next_elements:
            # print(element)

            if (not element.find('b')):

                # b태그가 연속으로 나오는 경우 (버린다.)
                if (count == 1):
                    count = 0
                    continue
                # 텍스트 이후 b태그가 나오는 경우 (count refresh)
                elif (count == 2):
                    count = 0
                # b태그 이후 b태그 속 텍스트가 출력되는 경우
                elif (count == 0):
                    count = 1
            else:
                # b태그 이후 텍스트가 나오는 경우
                # count updated
                # 정보 저장
                if (count == 1):
                    charactor = element.get_text()
                    charactor = charactor.strip().replace(" (CONT'D)", '').replace(" (CONT D)", '').replace("(CONT'D)",
                                                                                                            '')
                    # print(charactor)
                    count = 2


                # b태그의 텍스트 내용
                elif (count == 2):
                    script = element.get_text()
                    script = ' '.join(script.replace('\r', '').replace('\n', '').strip().split())
                    # print(script)
                    print(charactor + " | " + script)
                    try:
                        script_file.write(charactor + " | " + script + "\n")
                    except:
                        print('error')
                        print(complete_name)
                        os.remove(complete_name)
                    count = 0
        script_file.close()


def main():
    # 영화 제목을 스트링으로 넣어주세요.
    # 현재 장르 필요 없어져서 장르 파라미터 제거
    # 영화 제목만 넣어주심 됩니다.
    crawler = IMSDBMovieScriptCrawler("data/scripts")
    crawler.run("127 Hours")


if __name__ == "__main__":
    main()
