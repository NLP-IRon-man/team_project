import os
from turtle import down
from urllib import response
import requests
from bs4 import BeautifulSoup
import urllib3

url_crime = 'https://imsdb.com/genre/Crime'
url_romance = 'https://imsdb.com/genre/Romance'

try:
    os.makedirs(os.path.dirname(os.path.abspath(__file__)) +
                '/movie_scripts/crime_movies')
    os.makedirs(os.path.dirname(os.path.abspath(__file__)) +
                '/movie_scripts/romance_movies')
    os.makedirs(os.path.dirname(os.path.abspath(__file__)) +
                '/movie_scripts/action_movies')
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


def convert_movie_name(movie_name_list):

    for i in range(len(movie_name_list)):
        movie_name_list[i] = movie_name_list[i].replace(" ", "-")

    return movie_name_list


def make_script_url(movie_name_list, genre):
    url_script = 'https://imsdb.com/scripts/'

    for movie_name in movie_name_list:
        download_txt(movie_name, url_script + movie_name + '.html', genre)


def download_txt(movie_name, movie_sciprt_url, genre):
    http = urllib3.PoolManager()
    response = http.request('GET', movie_sciprt_url)
    soup = BeautifulSoup(response.data, "html.parser")

    save_path = os.path.dirname(os.path.abspath(
        __file__)) + '/movie_scripts/'+genre+'_movies'
    file_name = movie_name+'.txt'
    complete_name = os.path.join(save_path, file_name)

    count = 0

    print(movie_name)
    #script_file = open(complete_name,"w")

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
             charactor = charactor.strip().replace(" (CONT'D)", '').replace(" (CONT D)",'')
             #print(charactor)
             count = 2
            
             
          # b태그의 텍스트 내용
          elif(count == 2):
             script = element.get_text()
             script = ' '.join(script.replace('\r','').replace('\n','').strip().split())
             #print(script)
             print(charactor + " | " + script)
             count = 0


    #print(script_split_by_btag)

   #  try:
   #      script_file.write(soup.fid('pre').getText())
   #      #this part have to -> <b> get character name and next script name
   #      if(os.path.getsize(complete_name) == 0):
   #          os.remove(complete_name)
   #  except:
   #      print('error')
   #      print(complete_name)
   #      os.remove(complete_name)
   #  script_file.close()


def main():
   #change movie name
   make_script_url(["Black-Panther"], "action")


if __name__ == "__main__":
   main()
