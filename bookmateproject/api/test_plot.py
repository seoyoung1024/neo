import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


plt.rcParams['font.family'] = 'NanumBarunGothic'

# 예시 데이터: 실제 서비스와 유사한 구조
example_data = [
    {'연도': 2020, '주제분류': '일본문학', '대출수': 4000},
    {'연도': 2021, '주제분류': '일본문학', '대출수': 3500},
    {'연도': 2022, '주제분류': '일본문학', '대출수': 1503},
    {'연도': 2023, '주제분류': '일본문학', '대출수': 1200},
    {'연도': 2020, '주제분류': '한국문학', '대출수': 3044},
    {'연도': 2021, '주제분류': '한국문학', '대출수': 2500},
    {'연도': 2022, '주제분류': '한국문학', '대출수': 3700},
    {'연도': 2023, '주제분류': '한국문학', '대출수': 3400},
    {'연도': 2020, '주제분류': '동물학', '대출수': 3003},
    {'연도': 2021, '주제분류': '동물학', '대출수': 2344},
    {'연도': 2022, '주제분류': '동물학', '대출수': 5094},
    {'연도': 2023, '주제분류': '동물학', '대출수': 3300},
]

df = pd.DataFrame(example_data)
pivot = df.pivot(index='연도', columns='주제분류', values='대출수')
colors = ["#ff1919", "#ff9900", "#ffd700", "#1f77b4", "#2ca02c", "#9467bd"]
label_color_map = {}
simplified_labels = {col: col for col in pivot.columns}
plt.figure(figsize=(10, 5))
for idx, col in enumerate(pivot.columns):
    label_color_map[col] = colors[idx % len(colors)]
    plt.plot(pivot.index, pivot[col], label=simplified_labels[col], color=label_color_map[col], linewidth=1.5, marker='o')
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9, frameon=False)
plt.title("Z세대 중심(17~29세) \n 독서 성향 분석 결과", fontsize=17, pad=30)
plt.xlabel("")
plt.ylabel("대출 수", fontsize=11, labelpad=8)
plt.xticks(pivot.index, fontsize=12)
plt.yticks(fontsize=10)
plt.grid(axis='y', alpha=0.4)
plt.tight_layout(rect=[0, 0, 0.85, 1])
ax = plt.gca()
ax.spines['left'].set_linewidth(1)
ax.spines['bottom'].set_linewidth(1)
ax.spines['top'].set_visible(False)
plt.savefig("test_graph.png", bbox_inches='tight')
plt.show()
