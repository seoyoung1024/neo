import urllib.request 
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt 

plt.rcParams['font.family'] = 'NanumBarunGothic'

url = 'https://www.moviechart.co.kr/rank/boxoffice'
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

infos = soup.find_all('div', attrs={'class': 'wArea space title'})
# print('-' * 50)
# print(infos)
# print('-' * 50)

mydata0 = [i for i in range(1, 20)]

result = []
title = soup.select("td.title")
for i in title:
    result.append(i.text.strip()) #제목
mydata1 = result
print(mydata1)

# result = []
# score = soup.select("td.redAc")
# for i in score:
#     result.append(i.text.strip())
# mydata2 = result
# print(mydata2)  #순위

result = []
reserv = soup.select("td.date") 
for i in reserv:
    result.append(i.text.strip())
mydata2 = result  #개봉일
print(mydata2)

result = []
reserv = soup.select("td.audience") 
for i in reserv:
    result.append(i.text.replace('명', '').replace(' ', '').replace('\n', '').replace('\r', ''))
mydata3 = result  #관객수
print(mydata3)

result = []
release = soup.select("td.cumulative")
for i in release:
    result.append(i.text.replace('명', '').replace(' ', '').replace('\n', '').replace('\r', ''))
mydata4 = result #누적관객수
print(mydata4)

result = []
release = soup.select("td.sales")
for i in release:
    result.append(i.text.replace('원', '').replace(' ', '').replace('\n', '').replace('\r', ''))
mydata5 = result #누적매출액
print(mydata5)

mycolumn = ['순위', '제목', '개봉일', '관객수', '누적관객수', '누적매출액']

myframe = pd.DataFrame(data = list(zip(mydata0, mydata1, mydata2, mydata3, mydata4, mydata5)), columns = mycolumn)
myframe = myframe.set_index(keys=['순위']) #순위컬럼을 인덱스로 바꿔줌
print(myframe)
# print('-' * 40)

filename = 'quiz_03_cgvMovie.csv'
myframe.to_csv(filename, encoding='utf8', index=False)
print(filename, ' saved...', sep='')
print('finished')

# dfmovie = myframe.reindex(columns=['제목', '관객수', '누적관객수'])
# print(dfmovie)

# mygroup0 = dfmovie['제목']
# mygroup1 = dfmovie['평점']
# mygroup1 = mygroup1.str.replace('%','')
# mygroup1 = mygroup1.str.replace('?','0')
# mygroup2 = dfmovie['예매율']
# mygroup2 = mygroup2.str.replace('%','')
# mygroup2 = mygroup2.str.replace('?','0')

# df = pd.concat([mygroup1, mygroup2], axis=1)
# df = df.set_index(mygroup0)
# df.columns = ['평점', '예매율']
# print(df)

# df.astype(float).plot(kind='barh', title='영화별 평점과 예매율', rot=0)
# filename = 'quiz_02_cgvMovieGraph.png'
# plt.savefig(filename, dpi=400, bbox_inches='tight')
# plt.show()
