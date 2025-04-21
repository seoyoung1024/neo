import requests
from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()

def extract_top_book_info(api_response: dict, year: int):
    docs = api_response.get('response', {}).get('docs', [])
    if not docs:
        return None

    sorted_docs = sorted(
        docs,
        key=lambda d: int(d['doc']['loan_count']),
        reverse=True
    )
    
    top_doc = sorted_docs[0]['doc']
    
    return {
        "year": year,
        "classNm": top_doc.get("class_nm", "Unknown"),
        "topBook": {
            "title": top_doc.get("bookname", "Unknown"),
            "loanCount": int(top_doc.get("loan_count", 0))
        }
    }
def get_age_range(age_group: int):
    """
    나이 그룹에 맞는 범위 계산
    """
    # 나이대 범위 설정
    age_ranges = {
        17: (17, 21),  # Z세대 후반
        22: (22, 26),  # Z세대 중심
        27: (27, 31),  # 밀레니얼 후반 / Z세대
        32: (32, 36),  # 밀레니얼 중반
        37: (37, 41),  # 밀레니얼 초반
    }
    
    # 기본값 
    return age_ranges.get(age_group, (17, 21))



@app.get("/genre-change/")
def genre_change_analysis(startDt: str = '2024-01-01', endDt: str = '2025-03-31', ageGroup: int = 17):
    external_api_url = 'https://data4library.kr/api/loanItemSrch'
    auth_key = '815893da4d07574fea55156108fd8dd25ebefebf72d0badabf822811e76c0ab8'

    # 날짜를 datetime으로 변환
    try:
        start_year = datetime.strptime(startDt, "%Y-%m-%d").year
        end_year = datetime.strptime(endDt, "%Y-%m-%d").year
    except ValueError:
        raise HTTPException(status_code=400, detail="날짜 형식은 YYYY-MM-DD 여야 합니다")

    results = []

    # 나이대 범위 가져오기
    from_age, to_age = get_age_range(ageGroup)

    for year in range(start_year, end_year + 1):
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        
        params = {
            'authKey': auth_key,
            'startDt': start,
            'endDt': end,
            'from_age': str(from_age),  
            'to_age': str(to_age),      
            'format': 'json'
        }

        try:
            res = requests.get(external_api_url, params=params)
            res.raise_for_status()
            api_data = res.json()
            year_data = extract_top_book_info(api_data, year)
            if year_data:
                results.append(year_data)
        except Exception as e:
            print(f"Error fetching data for {year}: {e}")

        print(f"요청받은 ageGroup: {ageGroup}")
        from_age, to_age = get_age_range(ageGroup)
        print(f"조회할 나이 범위: {from_age} ~ {to_age}")


        print(f"외부 API 응답 데이터: {api_data}")
        print(f"외부 API 요청 URL: {res.url}")

    if not results:
        raise HTTPException(status_code=404, detail="요청한 기간에 대한 데이터를 찾을 수 없습니다")

    return {
        "graphImageUrl": "https://yourdomain.com/static/trend_20to29.png",  # 실제 이미지 경로로 수정
        "dataByYear": results
    }