import pandas as pd
import matplotlib.pyplot as plt

# 📌 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumBarunGothic'

# 📂 CSV 불러오기
filename = 'loan_books_2015_20s1.csv'  # 네가 방금 만든 파일 이름
myframe = pd.read_csv(filename, encoding='utf-8-sig')  # 혹은 euc-kr
myframe = myframe.set_index('name')
print(myframe)

# 📈 라인 그래프 그리기
myframe.plot(
    title='2015년 20대의 독서 장르 분포',
    kind='bar',
    figsize=(12, 6),
    linewidth=2,
    legend=True
)

# 💾 그래프 저장
savefile = '2015_20s_reading_trend33.png'
plt.savefig(savefile, dpi=400, bbox_inches='tight')
print(savefile + ' saved')

# 📊 그래프 출력
plt.show()
