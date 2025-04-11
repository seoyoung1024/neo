import requests
import pandas as pd

# ✨ 여기에 너의 발급받은 API 키를 넣어줘!
auth_key = ''

# API 요청 파라미터 설정 (예: 2015년 20대)
params = {
    'authKey': auth_key,
    'startDt': '2015-01-01',
    'endDt': '2015-12-31',
    'age': 20,
    'pageNo': 1,
    'pageSize': 100,  # 최대 1000까지 가능
    'format': 'json'
}

# API 호출
url = 'http://data4library.kr/api/loanItemSrch'
response = requests.get(url, params=params)
data = response.json()

# 응답에서 도서 목록 추출
docs = data.get('response', {}).get('docs', [])

# 필요한 필드만 뽑아서 정제
rows = []
print(docs[0])
for item in docs:
    book_info = item.get('doc', {})  # 'doc' 안에 실제 책 정보가 있음

    book = {
        '도서명': book_info.get('bookname'),
        '저자명': book_info.get('authors'),
        '출판사': book_info.get('publisher'),
        '출판년도': book_info.get('publication_year'),
        'ISBN': book_info.get('isbn13'),
        '주제분류': book_info.get('class_nm'),
        'KDC코드': book_info.get('class_no')
    }

    rows.append(book)


# DataFrame으로 변환
df = pd.DataFrame(rows)

print("전체 응답 데이터 확인:")
# print(data)

print("docs 항목 길이:", len(docs))

# CSV 저장
filename = 'loan_books_2015_20s.csv'
df.to_csv(filename, index=False, encoding='utf-8-sig')
print(f'{filename} 저장 완료')
