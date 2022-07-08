import pandas as pd
import csv
import json
import numpy as np

train=pd.read_excel('/home/eugene131/waterpy/poppulation.xlsx')#인구, 물 양을 데이터로 읽어옴
f=open('/home/eugene131/waterpy/rez_시도.txt',"r")
f1=open('/home/eugene131/waterpy/wtater_ton_final.csv',"r")
water_ton=f1.readlines()#지역별 물 양을 읽어서 리스트로 저장
rezon_fi_check=[]#지역 최종 체크
water_ton_final=[]
only_water=[]

#각 리스트에 필요한 요소들을 추가해주기 위한 반복
for i in water_ton:
    temp_ton=[]
    temp_ton=i.split(',')#water_ton에 있는 요소들을 ,기준으로 나눠서
    if temp_ton[0]=='세종특별자치시':#세종시는 군, 구가 없기 때문에 별도로 처리
        water_ton_final.append(temp_ton[0]+"  ")#지역 이름과 공백 2개(엑셀 파일에 지역 이름 뒤에 공백 2개다 들어가 있음) 추가
        rezon_fi_check.append(temp_ton[0]+"  ")#지역 이름과 공백 2개(엑셀 파일에 지역 이름 뒤에 공백 2개다 들어가 있음) 추가
        water_ton_final.append(temp_ton[2])#지역의 물 양 추가
        only_water.append(temp_ton[2].replace('\n',''))#공백을 없앤 지역의 물양 추가

    else:        
        water_ton_final.append(temp_ton[0]+" "+temp_ton[1]+" ")#시도 이름+ 시군구 이름
        rezon_fi_check.append(temp_ton[0]+" "+temp_ton[1]+" ")#시도 이름+ 시군구 이름
        water_ton_final.append(temp_ton[2])#지역의 물 양
        only_water.append(temp_ton[2].replace('\n',''))#지역의 물 양에서 공백을 없앰

#나중에 시도 삭제하는데 사용
rezon_all=f.readline().split(',')

#인구수가 0명인 지역 삭제
delete_row_num=[np.where('0'==train)[0].tolist()]
train=train.drop(delete_row_num[0])

#시도 배너 삭제위한 함수
delete_row_num_re=train.loc[(train['지역'].isin(rezon_all))].index.tolist()#엑셀 파일에는 각 시도의 총 인구수가 먼저 드러나고, 그 아래에 시군구 인구수가 있다.
train=train.drop(delete_row_num_re)# 즉, 시도 배지역 배너에서 rezon_all에 들어있는 시도들 삭제해야 시군구의 리스트만 남는다. 그래서 지역 배너의 시도 삭제

sejong=train.loc[(train['지역'].isin(['세종특별자치시  ']))].index.tolist()[1]#세종시는 따로 처리

#필요 없는 데이터 삭제
delete_list=train.loc[~(train['지역'].isin(rezon_fi_check))].index.tolist()#중간중간 출장소같은 이상한 지역들이 있어서 삭제할 리스트에 추가
#세종시가 2개 있어서 위치 찾고 삭제 리스트에 추가
cunt=0
for i in delete_list: 
    if i==sejong:
        break
    cunt+=1
delete_list.append(cunt)
train=train.drop(delete_list)


train["물"]=only_water#물 배너 만들어서 톤 데이터 넣어줌

#1인당 물 사용가능 데이터 만들기, 데이터 프레임에 추가
perst_water_list=[]#1인당 사용 가능한 물 넣을 리스트
for i in train.loc[(train['지역'].isin(rezon_fi_check))].index.tolist():
    perst_water=float(train['물'][int(i)].replace('t',''))/float(train['인구수'][int(i)].replace(',',''))
    perst_water_list.append(int(perst_water*1000))#톤단위에서 리터 단위로 바꾸기 위해 *1000
train["1인당 사용 가능 물"]=perst_water_list#1인당 사용 가능한 물 배너, 데이터 추가
train = train.sort_values(['1인당 사용 가능 물'],ascending=False)#1인당 물 사용 가능량에 따라서 소팅


train.to_excel('물 비율.xlsx',index=False)#물 비율이라는 엑셀 만들어줌
f.close()
f1.close()