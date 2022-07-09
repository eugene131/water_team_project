import pandas as pd
import csv
import json
import numpy as np
#입력받은 지역을 찾아서 아웃풋 엑셀로 내보냄
a=[]
for i in range(0,10):
    find_data=[]
    find_data=input()
    a.append(find_data)

train=pd.read_excel('/home/eugene131/waterpy/w_file/물 비율.xlsx')#인구, 물 양을 데이터로 읽어옴
delete_list=train.loc[~(train['지역'].isin(a))].index.tolist()
train=train.drop(delete_list)
train.to_excel('output.xlsx',index=False)
