# 물 공모전
- 공통사항 
    - 대부분 함수에서 본인이 원하는 폴더 주소로 가도록 share_url부분만 변경해 주시면 됩니다.
1. water_running.sh
    - water_final_code 및 ton_and_pp실행
    - water_final_code 실행의 부산물인 final_csv및 final_text들을 삭제 해줌
    - ton_and_pp의 부산물인 water_ton을 삭제 해줌
2. water_final_code
    - 국민 재난 안전 포털의 급수 시설에서 비상급수 시설 수량을 크롤링 해옴
    - 크롤링 해오는 과정에서 단위는 톤으로 통일
    - 크롤링 해온 데이터들을 지역순으로 re_final_csv.csv파일에 담아줌
    - 시도별로 톤의 총량을 계산해서 water_ton_final.csv파일에 담아줌
    - 추가로 물 단위 나오는것 모두 받아서 wet_string에 저장해줌
4. ton_and_pp
    - poppulation.xlsx파일에서 지역별 인구수를 받아옴
    - water_ton_final.csv에서 지역별 비상급수량을 받아옴
    - 받아온 두 정보를 이용해 1인당 사용가능 물 비율을 계산해줌
    - 결과를 '물 비율'.xlsx에 받아줌
5. find.py
    - 지역을 입력받아서 그 지역 정보만 아웃풋 파일로 내보냄
    - 보고서 작성시 필요한 정보 추출 빠르게 하기 위해 사용
6. water_ton_notton
    - wet_string에서 정보를 읽어 단위를 하나씩만 보이게 한 후 water.txt파일로 제공
    - 물의 단위가 톤이 아닌 것들이 무엇이 있는지 확인해줌
7. do_persent
    - '물 비율'.xlsx파일과 water_ton_final.csv, rez_시도.txt파일을 받아서 시도_퍼센트.csv로 
    - 시도 단위로 1인당 사용가능 물 양이 25L보다 작은 지역의 비율을 보여줌
8. excel 폴더
    - 한국수자원공사가뭄피해내역.csv
    - -> 공공데이터 포털에서 한국수자원공사의 07~20년도의 가뭄피해내역 파일을 이용하였습니다.

Datas.xlsx
    -> 공공데이터를 Colab(Jupyter Notebook) 환경에서 작업하여 피해가 발생한 각 지역에 대하여 역대 피해량을 통합하고, 점수화하여 가뭄피해의 심각도를 순위로 나타내었습니다.

9. Colab 폴더

    - K_water_DroughtInfo.ipynb (k_water_droughtinfo.py)
    -> Google Colab 환경에서 데이터 처리 과정을 담은 코드입니다.
   1. 년도별 구분 가뭄피해 발생내역
   2. 역대 가뭄피해 발생내역
   크게 두 결과물을 만드는 코드입니다.

   한국수자원공사가뭄피해내역.csv 데이터를 import하여 사용하시면 됩니다.


    - Colab 링크를 첨부합니다.
        - https://colab.research.google.com/drive/14JS5H9YW1dp061lUuVUh9NLHRZohHOzD?usp=sharing


10. Tableau 폴더

    - Datas.xlsx와 비상급수현황자료를 Tableau의 지오코딩을 이용하여 데이터를 가시화하였습니다.
