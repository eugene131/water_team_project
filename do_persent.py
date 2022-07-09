import pandas as pd
import csv
import json
import numpy as np

train=pd.read_excel('/home/eugene131/waterpy/w_file/물 비율.xlsx')#인구, 물 양을 데이터로 읽어옴
f=open('/home/eugene131/waterpy/w_file/wtater_ton_final.csv',"r")
f_sido=open('/home/eugene131/waterpy/w_file/rez_시도.txt',"r")
f_persent=open('/home/eugene131/waterpy/w_file/시도_퍼센트.csv',"w")

#두 종류 다 시군구 파악하는 코드임
rezon_all1=[]
for i in f.readlines():
    temp_ton=[]
    temp_ton=i.split(',')
    rezon_all1.append(temp_ton[0]+" "+temp_ton[1]+" ")
rezon_all2=train['지역'].unique().tolist()

#시도를 나눠서 리스트에 넣고
sido_list=f_sido.readline().split()

#반복
for i in sido_list:#시도별로 확인해서
    tr=train[train['지역'].str.contains(i)]
    water=tr['1인당 사용 가능 물'].unique().tolist()
    sum=0
    cunt=0#25리터 미만 수
    for j in water:#25리터 미만이면 카운트++
        if 25>int(j):
            cunt+=1
        sum+=1
    #분수 퍼센테이지화, 소숫점 둘째자리까지        
    persent=float(cunt/sum)
    persent=persent*100
    persent=round(persent,2)
    f_persent.write(i+","+str(persent)+"\n")#csv파일로 만들어줌

f.close()
f_persent.close()
f_sido.close()

#delete_list=train.loc[~(train['지역'].isin(a))].index.tolist()
#train=train.drop(delete_list)


#train.to_excel('do_pers_output.xlsx',index=False)
