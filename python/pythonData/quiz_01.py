from bs4 import BeautifulSoup

html = open('/work/neo/html/source/5/ex5-10.html', 'r', encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')
tbody = soup.find('tbody')  # 먼저 tbody를 soup에서 찾아줌
tds = tbody.find_all('td')  # 그 다음 td를 찾는 거야


# print(tds)

from pandas import Series
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'NanumBarunGothic'

mylist = tds
print(mylist)
print('-' * 50)

tds1 = np.reshape(a, (2, 2))
print(tds1)

# myseries = Series(data=mylist, index=myindex)
# mylim = [0, myseries.max() + 10]
# myseries.plot(title='금월 실적', kind='line', ylim=mylim, grid=False, rot=40, use_index=True, color=['b'])

# filename = 'quiz_01_scoreGraph.png'
# plt.savefig(filename, dpi=400, bbox_inches='tight')
# print(filename + ' saved')
# plt.show()
