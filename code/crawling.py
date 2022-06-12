import os
from turtle import down
from urllib import response
import requests
from bs4 import BeautifulSoup
import urllib3

try:
    os.makedirs(os.path.dirname(os.path.abspath(__file__)) +
                '/scripts')
except:
    print('Already exists folder')


def get_movie_name(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "html.parser")
    movie_name_list = []

    for i in range(len(soup.find_all('p'))):
        movie_name_list.append(soup.find_all('p')[i].contents[0].getText())

    return convert_movie_name(movie_name_list)

# ismdb에서는 영화 제목이 스페이스바 대신 -를 사용
# 이를 변환시켜주는 코드
# 현재 사용할 필요 x
def convert_movie_name(movie_name):

    movie_name = movie_name.replace(" ", "-")

    return movie_name

# 자동으로 url 생성 및 다운로드 진행
# 메인에서처럼 사용하면 됩니다.
def make_script_url(movie_name):
    movie_name = movie_name.replace(" ", "-")
    url_script = 'https://imsdb.com/scripts/'

    download_txt(movie_name, url_script + movie_name + '.html')


def download_txt(movie_name, movie_sciprt_url):
    http = urllib3.PoolManager()
    response = http.request('GET', movie_sciprt_url)
    soup = BeautifulSoup(response.data, "html.parser")

    save_path = os.path.dirname(os.path.abspath(
        __file__)) + '/scripts'
    file_name = movie_name+'.txt'
    complete_name = os.path.join(save_path, file_name)

    count = 0

    print(movie_name)
    script_file = open(complete_name,"w")

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
       #print(element)
       
       if(not element.find('b')):

          # b태그가 연속으로 나오는 경우 (버린다.)
          if(count == 1):
             count = 0
             continue
          # 텍스트 이후 b태그가 나오는 경우 (count refresh)
          elif(count == 2):
             count = 0
          # b태그 이후 b태그 속 텍스트가 출력되는 경우 
          elif(count == 0):
             count = 1
       else:
          # b태그 이후 텍스트가 나오는 경우 
          # count updated
          # 정보 저장
          if(count == 1):
             charactor = element.get_text()
             charactor = charactor.strip().replace(" (CONT'D)", '').replace(" (CONT D)",'').replace("(CONT'D)", '')
             #print(charactor)
             count = 2
            
             
          # b태그의 텍스트 내용
          elif(count == 2):
             script = element.get_text()
             script = ' '.join(script.replace('\r','').replace('\n','').strip().split())
             #print(script)
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
   make_script_url("It")


if __name__ == "__main__":
   main()
