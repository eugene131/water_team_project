from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
import sys
from selenium.webdriver import ActionChains
import pandas as pd
import csv
import json
from threading import Thread

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

#7개의 스레드를 만들거기 때문에 드라이버 7개 생성
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/contents/civil_defense/SDIJKM1401.html?menuSeq=56')#드라이버 연결
driver2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# #driver2 = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver2.get('https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/contents/civil_defense/SDIJKM1401.html?menuSeq=56')#드라이버 연결
# #driver3 = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver3 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver3.get('https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/contents/civil_defense/SDIJKM1401.html?menuSeq=56')#드라이버 연결
# #driver4 = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver4 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver4.get('https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/contents/civil_defense/SDIJKM1401.html?menuSeq=56')#드라이버 연결
# #driver5 = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver5 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver5.get('https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/contents/civil_defense/SDIJKM1401.html?menuSeq=56')#드라이버 연결
# #driver6 = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver6 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver6.get('https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/contents/civil_defense/SDIJKM1401.html?menuSeq=56')#드라이버 연결
# #driver7 = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver7 = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver7.get('https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/contents/civil_defense/SDIJKM1401.html?menuSeq=56')#드라이버 연결
driver.implicitly_wait(10)
sleep(0.1)

#page 소스 읽어서
res_resz=driver.page_source
souprz = BeautifulSoup(res_resz,'html.parser')#해당 부분읽어서 html형식으로
#print(souprz)
rezion = souprz.find('select',title="시도선택")#읽어 들인 것들 중 시도 선택 배너에 있는거 다 읽어들이기
driver.implicitly_wait(100)
sleep(0.1)

rezion_all=rezion.get_text('\n').split('\n')#시도 선택 배너에 있는 데이터 읽어들이기, 정리
rezion_all.pop(0)
rezion_all.pop(0)
rezion_all.pop(0)
print(rezion_all)

#각 시도 읽어들인거 하나씩 클릭해서 그 아래에 뜨는 시군구 선택 읽고 정리
final_rezion=[]#최종적으로 첫번째에 시도, 그 다음부터 군구 있는 리스트 만들기위함
for i in rezion_all:
    #print(i)
    driver.find_element(By.XPATH,'//*[@id="sbRnArea1"]/option[text()="'+i+'"]').click()
    driver.implicitly_wait(100)
    sleep(0.3)
    res2 = driver.page_source
    sigoon = BeautifulSoup(res2, 'html.parser')
    sigoon1 = sigoon.find('select', title="시군구선택")
    
    sigoon_all=sigoon1.get_text('\n').split('\n')
    for j in range(0,3):
        sigoon_all.pop(0)
    #print(sigoon_all)
    a=[]
    a=sigoon_all
#    print(a)
    final_rezion.append(a)
print(rezion_all)
final_rezion[14].pop(14)#이상하게 영양시만 안되서 일단 빼둠
for i in final_rezion:
    print(i)

    #num1 부터 num2까지 final_rezion에 들어있는 시도 데이터 읽어들임
#f_name에txt파일로 저장, f1에 csv파일로 저장 f2에 급수량만 군구별로 저장
#txt파일은 csv파일이 열리지 않을 때, 오류 부분 직관적으로 확인하기 위함
#driver가 따로 필요하기 때문에 driver를 받아서 실행
def th_demo(num1,num2, f_name,f1_name,f2_name,driver):
    global final_rezion, rezion_all#final_rizion=시도, rezion_all=시군구 데이터
    full_data=[]
    f= open(f_name,"w")
    f1=open(f1_name,"w")
    f2=open(f2_name,"w")
    
    if num1==0:
        f1.write('시도,군구,신주소,구주소,이름,용량\n')#csv파일에 구분 주기 위한 배너

    check_list_eq_ton=["t(톤)/시간","㎥/시간","t(톤)","㎥/일","㎥","톤/일","㎡","m","길이","㎜","㎥/년","기타","HP","ton"]#톤 단위 t로 통일 시키기 위해서 나오는 단위 전부 찾아서 만
    #check_list_not_eq_ton=["t(톤)/시간","㎥/시간"]
    for i in range(num1,num2):#총 17개의 시, 도가 있음, num1 시도 부터 num2 시도까지
       
        if i!=7:
        
            for j in final_rezion[i]:#군구 전부 하나씩 넣어주면서 돌아감
                water_wi=0# 시군구별 물 무게 계산 하기 위해서
                
                driver.find_element(By.XPATH,'//*[@id="sbRnArea1"]/option[text()="'+rezion_all[i]+'"]').click()#시도 클릭
                driver.implicitly_wait(100)
                driver.find_element(By.XPATH,'//*[@id="sbRnArea2"]/option[text()="'+j+'"]').click()#군구 클릭
                driver.implicitly_wait(100)
                driver.find_element(By.XPATH,'//*[@id="btnSearchOk"]').click()#검색 버튼 클릭
                driver.implicitly_wait(100)
                sleep(0.3)#로딩될 동안 대기

                while True:#페이지가 마지막 페이지인지 확인용
                    res=driver.page_source
                    soup = BeautifulSoup(res, 'html.parser')
                    check1 = soup.find('span', class_='nowNum')#페이지 수 확인용
                    check2 = soup.find('span', id="tbpagetotal")
                    ch1=check1.text#현재 페이지수
                    ch2=check2.text.strip('/')#총 페이지 수

                #읽어서 출력하는 부분
                    title = soup.find('title')#타이틀 출력이 필요할 때를 대비해서
                    p_data = soup.find('div',class_='content')#div에 클래스가 content인 부분
                    pp_data=p_data.find('tbody')#div에 클래스가 content인 부분 중에 tbody부분에 원하는 데이터가 있음
                    for adad in range(10):#페이지당 데이터는 최대 10개
                        adr1=pp_data.select_one('tr:nth-of-type('+str(adad+1)+')')#이 부분에 각 지역의 주소, 이름, 급수량 등이 있음
                        if adr1==None:
                            break
                        adr2=adr1.select('td:nth-of-type(1)')#주소
                        name=adr1.select('td:nth-of-type(2)')#그 장소 이름
                        water=adr1.select('td:nth-of-type(3)')#물 양
                        
                        for k in range(len(adr2)):
                            adr2_2=adr2[k].text.replace(',',' ').replace('지도보기','').split('구주소 :')#주소를 신주소와 구주소로 나누고, '지도보기' 단어를 지움
                            a=water[k].text#물 양을 텍스트로
                            string_wet = ''.join([r for r in a if not r.isdigit()])#물양의 단위 확인하기 위해
                            string_int = int(''.join([r for r in a if  r.isdigit()]))#물 양을 int형으로
                            
                            if string_wet in check_list_eq_ton:#물 단위를 톤으로 변경
                                string_wet="t(톤)"
                            else:
                                string_int=string_int*24#원래는 24를 곱했으나 위에 초반 코드 바꿔서 이부분 실행되지X
                                string_wet="t(톤)"
                            
                            water_wi+=string_int#물의 양 계속 더해줌
                            a=str(string_int)+string_wet
                            
                            f1.write(rezion_all[i]+','+j+','+adr2_2[0].replace('신주소 :','')+','+adr2_2[1].replace('신주소 :','')+','+name[k].text.replace(',',' ')+','+a+'\n')
                            f.write(rezion_all[i]+','+j+','+adr2_2[0].replace('신주소 :','')+','+adr2_2[1].replace('신주소 :','')+','+name[k].text.replace(',',' ')+','+a+'\n')
                            
                          #  print(rezion_all[i]+','+j+','+adr2_2[0].replace('신주소 :','')+','+adr2_2[1].replace('신주소 :','')+','+name[k].text.replace(',',' ')+','+a)
                    
                    if (int(ch1)==int(ch2)):#물 양을 시군구 별로 물 저장용 f2에 저장
                        f2.write(rezion_all[i]+','+j+','+str(water_wi)+"t\n")
                        break
                    
                    driver.find_element(By.XPATH,'//*[@id="apagenext"]').click()#페이지 넘기는거 클릭
                    driver.implicitly_wait(100)
                    sleep(0.3)
    #세종시는 군구가 없기 때문에 따로 처리
    #위 설명과 동일한 코드임  
        else:
            #print("세종시 확인용")
            driver.find_element(By.XPATH,'//*[@id="sbRnArea1"]/option[text()="세종특별자치시"]').click()
            driver.implicitly_wait(100)
            driver.find_element(By.XPATH,'//*[@id="btnSearchOk"]').click()
            driver.implicitly_wait(100)
            sleep(0.3)
            water_wi=0
            while True:
                    res=driver.page_source
                    soup = BeautifulSoup(res, 'html.parser')
                    check1 = soup.find('span', class_='nowNum')
                    check2 = soup.find('span', id="tbpagetotal")
                    ch1=check1.text
                    ch2=check2.text.strip('/')

                    title = soup.find('title')
                    #print(title.get_text())
                    p_data = soup.find('div',class_='content')#, class_='ellipsis mapView_link')
                    pp_data=p_data.find('tbody')
                    
                    for adad in range(10):
                        adr1=pp_data.select_one('tr:nth-of-type('+str(adad+1)+')')
                        if adr1==None:
                            break
                        adr2=adr1.select('td:nth-of-type(1)')
                        name=adr1.select('td:nth-of-type(2)')
                        water=adr1.select('td:nth-of-type(3)')
                        
                        for k in range(len(adr2)):
                            adr2_2=adr2[k].text.replace(',',' ').replace('지도보기','').split('구주소 :')
                            a=water[k].text
                            string_wet = ''.join([i for i in a if not i.isdigit()])
                            
                            string_int = int(''.join([i for i in a if  i.isdigit()]))
    
                            if string_wet in check_list_eq_ton:
                                string_wet="t(톤)"
                            else:
                                string_int=string_int*24
                                string_wet="t(톤)"
                            water_wi+=string_int
                            a=str(string_int)+string_wet

                            f1.write(rezion_all[i]+','+j+','+adr2_2[0].replace('신주소 :','')+','+adr2_2[1].replace('신주소 :','')+','+name[k].text.replace(',',' ')+','+a+'\n')
                            f.write(rezion_all[i]+','+j+','+adr2_2[0].replace('신주소 :','')+','+adr2_2[1].replace('신주소 :','')+','+name[k].text.replace(',',' ')+','+a+'\n')
                           # print(rezion_all[i]+','+j+','+adr2_2[0].replace('신주소 :','')+','+adr2_2[1].replace('신주소 :','')+','+name[k].text.replace(',',' ')+','+a)

                    # for r in ppp_data:
                    #     print(r.text)
                    if (int(ch1)==int(ch2)):
                        f2.write(rezion_all[i]+','+j+','+str(water_wi)+"t\n")
                        break
                    
                    driver.find_element(By.XPATH,'//*[@id="apagenext"]').click()#페이지 넘기는거 클릭
                    driver.implicitly_wait(100)
                    
                    sleep(0.3)
    f.close()
    f1.close()
    driver.quit()

#쓰레드별로 실행
th1=Thread(target=th_demo,args=(0,1,"/home/eugene131/waterpy/final_text1.txt","/home/eugene131/waterpy/final_csv1.csv","/home/eugene131/waterpy/water_ton1.csv",driver))
th1.start()

th5=Thread(target=th_demo,args=(8,9,"/home/eugene131/waterpy/final_text5.txt","/home/eugene131/waterpy/final_csv5.csv","/home/eugene131/waterpy/water_ton5.csv",driver5))
th5.start()

th2=Thread(target=th_demo,args=(1,2,"/home/eugene131/waterpy/final_text2.txt","/home/eugene131/waterpy/final_csv2.csv","/home/eugene131/waterpy/water_ton2.csv",driver2))
th2.start()

th3=Thread(target=th_demo,args=(2,6,"/home/eugene131/waterpy/final_text3.txt","/home/eugene131/waterpy/final_csv3.csv","/home/eugene131/waterpy/water_ton3.csv",driver3))
th3.start()

th4=Thread(target=th_demo,args=(6,8,"/home/eugene131/waterpy/final_text4.txt","/home/eugene131/waterpy/final_csv4.csv","/home/eugene131/waterpy/water_ton4.csv",driver4))
th4.start()

th6=Thread(target=th_demo,args=(9,13,"/home/eugene131/waterpy/final_text6.txt","/home/eugene131/waterpy/final_csv6.csv","/home/eugene131/waterpy/water_ton6.csv",driver6))
th6.start()

th7=Thread(target=th_demo,args=(13,17,"/home/eugene131/waterpy/final_text7.txt","/home/eugene131/waterpy/final_csv7.csv","/home/eugene131/waterpy/water_ton7.csv",driver7))
th7.start()

th1.join()
th2.join()
th3.join()
th4.join()
th5.join()
th6.join()
th7.join()


#쓰레드로 파일 7개 생성 -> 7개 파일 하나로 합쳐주는 작업
f1= open("/home/eugene131/waterpy/final_csv1.csv","r")
f2= open("/home/eugene131/waterpy/final_csv2.csv","r")
f3= open("/home/eugene131/waterpy/final_csv3.csv","r")
f4= open("/home/eugene131/waterpy/final_csv4.csv","r")
f5= open("/home/eugene131/waterpy/final_csv5.csv","r")
f6= open("/home/eugene131/waterpy/final_csv6.csv","r")
f7= open("/home/eugene131/waterpy/final_csv7.csv","r")
f_fi= open("/home/eugene131/waterpy/re_final_csv.csv","w")

wf1=open("/home/eugene131/waterpy/water_ton1.csv","r")
wf2=open("/home/eugene131/waterpy/water_ton2.csv","r")
wf3=open("/home/eugene131/waterpy/water_ton3.csv","r")
wf4=open("/home/eugene131/waterpy/water_ton4.csv","r")
wf5=open("/home/eugene131/waterpy/water_ton5.csv","r")
wf6=open("/home/eugene131/waterpy/water_ton6.csv","r")
wf7=open("/home/eugene131/waterpy/water_ton7.csv","r")
wf_fi=open("/home/eugene131/waterpy/wtater_ton_final.csv","w")

for i in wf1.readlines():
    wf_fi.write(i)
for i in wf2.readlines():
    wf_fi.write(i)
for i in wf3.readlines():
    wf_fi.write(i)
for i in wf4.readlines():
    wf_fi.write(i)
for i in wf5.readlines():
    wf_fi.write(i)
for i in wf6.readlines():
    wf_fi.write(i)
for i in wf7.readlines():
    wf_fi.write(i)
for i in f1.readlines():
    f_fi.write(i)
for i in f2.readlines():
    f_fi.write(i)
for i in f3.readlines():
    f_fi.write(i)
for i in f4.readlines():
    f_fi.write(i)
for i in f5.readlines():
    f_fi.write(i)
for i in f6.readlines():
    f_fi.write(i)
for i in f7.readlines():
    f_fi.write(i)
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
f7.close()
f_fi.close()
wf1.close()
wf2.close()
wf3.close()
wf4.close()
wf5.close()
wf6.close()
wf7.close()
wf_fi.close()
print('end water')