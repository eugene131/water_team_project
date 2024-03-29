# -*- coding: utf-8 -*-
"""K-water_DroughtInfo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14JS5H9YW1dp061lUuVUh9NLHRZohHOzD

# 2007~2020까지의 가뭄 발생에 대한 피해내역
공공데이터포털의 가뭄피해내역 csv파일 이용 (raw data)

피해종료일이 0인 것과 피해인구가 0인 자료들은 이상치로 여겨 제외했습니다.

##사용한 데이터
*한국수자원공사가뭄피해내역(07~20)*
*한국수자원공사*


##output 데이터
1. 년도별 구분 가뭄피해 발생내역
2. 역대 가뭄피해 발생내역

#드라이브 마운트
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np

Drought_df = pd.read_csv('/content/drive/MyDrive/K-water/한국수자원공사가뭄피해내역.csv',encoding='cp949')

Drought_df.columns

"""#데이터 전처리"""

#데이터 전처리 - 피해시작일, 피해종료일의 str to datetime, 피해지속기간 column 추가,
# 피해종료일 누락 제외, 피해인구 0 제외
def data_preprocessing():
  Drought_df['피해시작일']=pd.to_datetime(Drought_df['피해시작일'])
  Drought_df['피해종료일']=pd.to_datetime(Drought_df['피해종료일'])
  Drought_df['피해지속기간'] = Drought_df['피해종료일']-Drought_df['피해시작일']
for i in range(len(Drought_df['피해인구'])):
    if Drought_df['피해인구'][i] == 0:
      print(i)
      Drought_df.drop(i)
      i -= 1

data_preprocessing()
Drought_df = Drought_df.dropna(how='any')

Drought_df
Drought_df['years']=Drought_df['피해시작일'].dt.year

"""#구현할 함수들
0. 년도별, 시도별, 시군구별, 읍면동별 검색
1. 년도별 발생지역 리스트
2. 년도별, 지역별 피해지속기간 리스트
3. (년도통합) 지역별 피해총인구, 피해총기간, 발생건수

#0 to 2 : 년도별 구분
"""

#1. 년도별 발생지역 리스트

# loc 변수를 시도, 시군구, 읍면동 바꿈에 따라 나오는 리스트가 바뀐다.

# 검색하고싶은 년도 입력
year = 2018

def location_per_year(currentyear):
  is_exist =[]
  # loc=Drought_df.loc[(Drought_df['years']==currentyear)]['시도']
  loc=Drought_df.loc[(Drought_df['years']==currentyear)]['시군구']
  #loc=Drought_df.loc[(Drought_df['years']==currentyear)]['읍면동']
  for i in loc:
    if i not in is_exist :
      is_exist.append(i)
    else:
      continue
  return is_exist

# print(location_per_year(year))

datas = pd.DataFrame(columns=['년도','지역', '총인구(명)', '횟수', '총기간(일)','최대피해일수'])
datas.loc[0]=['년도','지역', '총인구(명)', '횟수', '총기간(일)','최대피해일수']
# print(datas)

#2. 년도별, 지역별 피해지속기간 리스트

# 검색할 년도 입력

count = 1

for year in range(2007,2021):
  list1 = location_per_year(year)
  for i in list1:
    days_list = []
    pop_list = []
    location_df = Drought_df.loc[(Drought_df['시군구']==i)]
    highloc_list = location_df.loc[(location_df['years']==year)]['시도']
    days_list = location_df.loc[(location_df['years']==year)]['피해지속기간'].dt.days
    pop_list = location_df.loc[(location_df['years']==year)]['피해인구']

    length = len(days_list)+1
    total = sum(days_list)
    longest = max(days_list)
    shortest = min(days_list)
    pop = max(pop_list)

    print(length,total,longest,shortest,pop)
    totalpop = max(pop_list)
    j = 0
    # for j in range(len(days_list)):
    #   totalpop += days_list[j] * pop_list[j]
    # datas.loc[count]=[year,i,pop,length,total]
    count += 1

print(datas)
  # print(i)
  # print("\n총",length,"개 지역\n","최장가뭄지속기간",longest,"\n","최단 가뭄지속기간",shortest,"\n")
  # print("\n총",total,"일동안 지속\n")
  # print("평균",int(total/length),"일동안 지속\n")
  # print("next\n\n\n\n\n\n")

"""#3: 지역별 년도통합 자료


"""

Drought_df['지역명']=Drought_df['시도']+" "+Drought_df['시군구']

is_exist=[]
for i in range(len(Drought_df['지역명'])):
  if Drought_df['지역명'][i] in is_exist:
    continue
  else:
    is_exist.append(Drought_df['지역명'][i])

datas = pd.DataFrame(columns=['지역', '총 피해인구(명)', '총 발생건수', '총기간(일)','최대피해일수(건)','최대피해인구(건)'])
datas.loc[0]=['지역', '총 피해인구(명)', '총 발생건수', '총기간(일)','최대피해일수(건)','최대피해인구(건)']
print(datas)

count = 0
for i in is_exist:
  count += 1
  population = Drought_df.loc[(Drought_df['지역명']==i)]['피해인구']
  day = Drought_df.loc[(Drought_df['지역명']==i)]['피해지속기간']
  totpop = sum(population)
  maxpop = max(population)
  cases = len(day)

  totday = sum(day.dt.days) + cases
  maxday = max(day.dt.days) + 1
  # print("인구",population,"\n날짜",days,"\n건수",len(days))
  print(totpop, totday,len(population),len(day),maxpop,maxday)
  datas.loc[count]=[i,totpop,len(day),totday,maxday,maxpop]

print(datas)

"""# 데이터 점수화"""

#if necessary
#datas = datas.drop(0)

maxcases = max(datas['총 발생건수'])
maxpopulation = max(datas['총 피해인구(명)'])
maxdays = max(datas['총기간(일)'])

datas['발생건수-백분위'] = datas['총 발생건수']/maxcases
datas['피해인구-백분위'] = datas['총 피해인구(명)']/maxpopulation
datas['총기간-백분위'] = datas['총기간(일)']/maxdays

datas = datas.round({'발생건수-백분위':4,'피해인구-백분위':4,'총기간-백분위':4})

datas['rank-발생건수'] = datas['발생건수-백분위'].rank(ascending=False)
datas['rank-피해인구'] = datas['피해인구-백분위'].rank(ascending=False)
datas['rank-총기간'] = datas['총기간-백분위'].rank(ascending=False)

datas['points'] = datas['발생건수-백분위']*10 + datas['피해인구-백분위']*10 + datas['총기간-백분위']*10

datas['RANK'] = datas['points'].rank(ascending=False)

datas

datas['시도'] = datas.지역.str.split(' ').str[0]
datas['시군구'] = datas.지역.str.split(' ').str[1]

datas

datas2 = datas.sort_values(by=['총 발생건수'],axis=0,ascending=False)
datas3 = datas.sort_values(by=['총 피해인구(명)'],axis=0,ascending=False)

datas2

"""# 데이터 자료화"""

# datas.to_csv('/content/drive/MyDrive/K-water/datas.csv',header=False,index=False,encoding='utf-8-sig')
# datas2.to_csv('/content/drive/MyDrive/K-water/TotalCasesdata.csv',header=False,index=False,encoding='utf-8-sig')
# datas3.to_csv('/content/drive/MyDrive/K-water/TotalPopulationdata.csv',header=False,index=False,encoding='utf-8-sig')

"""#비상급수 지역구분
tableau 지오코딩을 위한 구분

"""



dataf = pd.read_excel('/content/drive/MyDrive/K-water/waterfinal.xlsx')

dataf

dataf['시군구'] = dataf.지역.str.split(' ').str[1]
dataf['시도'] = dataf.지역.str.split(' ').str[0]

dataf

dataf.to_excel('/content/drive/MyDrive/K-water/waterfinal.xlsx',header=False,index=False)