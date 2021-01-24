import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import urllib.request
import csv
import os.path


# 전역변수
global url
url = "https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl"


# 메인 함수
def main(keyword , end_count , save_path):

    local_path = fr'{save_path}\\{keyword}'

    driver_path = None # 웹 드라이버가 저장된 경로를 입력해주세요 #


    # 웹 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 로깅 비활성화
    # options.add_argument('headless') # 헤드리스 옵션사용시 주석을 해제해주세요
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko") # 유저헤더
    driver = webdriver.Chrome(
        driver_path, options=options) # webdriver 파일을 지정해주세요
    # 옵션문 끝


    
    driver.get(url) # 구글 이미지 검색 사이트 오픈
    elem = driver.find_element_by_name("q") # 검색창 활성화
    elem.send_keys(keyword)  # 검색
    elem.send_keys(Keys.RETURN) 

    SCROLL_PAUSE_TIME = 1  # 스크롤 깊이 측정하기

    last_height = driver.execute_script("return document.body.scrollHeight")

    if end_count > 20: # 저장할 이미지가 20개 이하라면 스크롤 내리기 생략
        while True:  # 스크롤 끝까지 내리기
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")  # 페이지 로딩 기다리기
            time.sleep(SCROLL_PAUSE_TIME)  # 더 보기 요소 있을 경우 클릭하기
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                try:
                    driver.find_element_by_css_selector(".mye4qd").click()
                except:
                    break

            last_height = new_height  

    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd") # 이미지 찾고, 다운받기


    if not os.path.isfile(local_path + '_' +'result.csv'): # 해당경로에 파일이 없으면 
        f = open(local_path +'_' +'result.csv' ,'w',newline='') # 문자 추가
        wr = csv.writer(f)
        wr.writerow(['Time' , 'Keyword' , 'Count' , 'Url' , 'Title']) # csv 열 제목
    else:
        f = open(local_path +'_' +'result.csv' ,'a',newline='') # 파일 생성
        wr = csv.writer(f)

    count = 1 # 이미지의 첫번째 

    for image in images:

        if count == end_count + 1: 
            break
        image.click()
        time.sleep(2)
        try:
            imgUrl = driver.find_element_by_xpath(
                "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img").get_attribute('src') # 이미지 주소
            urllib.request.urlretrieve(imgUrl, local_path + str(count) + ".jpg")

            img_path = driver.find_element_by_xpath(
                "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[3]/div[2]/a").get_attribute('href') # 이미지 링크
            
            img_title = driver.find_element_by_xpath(
                "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[3]/div[2]/a").get_attribute('title') # 이미지 타이틀

            time_get = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime())

            wr.writerow([time_get , keyword , str(count) , img_path , img_title])

        except: 
            pass

        count = count + 1

    f.close()
    driver.close()





if __name__ == '__main__':

    keyword = input('검색어를 입력하세요 : ')
    end_count = int(input('저장할 이미지 갯수를 입력하세요 : '))
    save_path = input('저장할 경로를 입력하세요 : ')

    res = requests.get(url) # 연결 확인

    if res.status_code == 200:
        print('정상 크롤링을 시작합니다')

        start_time = time.time()
        main(keyword , end_count , save_path)
        end_time = time.time()

        print('- - - - 작업완료 - - - -')
        print('작업시간 : {0}'.format(end_time - start_time))

    else:
        print('인터넷 연결을 확인해주세요')


    

