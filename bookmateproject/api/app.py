import requests, json
from fastapi import FastAPI, HTTPException
from datetime import datetime
from fastapi.staticfiles import StaticFiles
import os
import pandas as pd
import platform
import pymysql
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, 'secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["[http://192.168.1.21](http://192.168.1.21):8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = "static"
os.makedirs(static_dir, exist_ok=True)  # static 폴더가 없으면 생성
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# --- MySQL 연결/캐싱 함수 추가 ---
def get_db_connection():
    db_info = {
        "host": get_secret("Mysql_Hostname"),
        "user": get_secret("Mysql_User"),
        "port": get_secret("Mysql_Port"),
        "password": get_secret("Mysql_Password"),
        "database": get_secret("Mysql_DBname"),
        "charset": "utf8mb4",
        "autocommit": True,
        "cursorclass": pymysql.cursors.DictCursor
    }
    return pymysql.connect(**db_info)

def get_cached_genre_analysis(age_group, start_dt, end_dt):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT result_json FROM genre_analysis
                WHERE age_group=%s AND start_dt=%s AND end_dt=%s
                ORDER BY created_at DESC LIMIT 1
            """
            cursor.execute(sql, (age_group, start_dt, end_dt))
            row = cursor.fetchone()
            if row:
                return json.loads(row["result_json"])
    finally:
        conn.close()
    return None

def save_genre_analysis(age_group, start_dt, end_dt, start_year, end_year, result_json):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO genre_analysis (age_group, start_dt, end_dt, start_year, end_year, result_json, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                    result_json=VALUES(result_json),
                    created_at=NOW(),
                    start_year=VALUES(start_year),
                    end_year=VALUES(end_year)
            """
            cursor.execute(sql, (
                age_group, start_dt, end_dt, start_year, end_year, json.dumps(result_json, ensure_ascii=False)
            ))
    finally:
        conn.close()

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
    age_ranges = {
        17: (17, 21),  # Z세대 후반
        22: (22, 26),  # Z세대 중심
        27: (27, 31),  # 밀레니얼 후반 /Z세대 초입
        32: (32, 36),  # 밀레니얼 중반
        37: (37, 41),  # 밀레니얼 초반
    }
    return age_ranges.get(age_group, (17, 21))

def get_age_label(age_group: int):
    labels = {
        17: "Z세대 후반",
        22: "Z세대 중심",
        27: "밀레니얼 후반",
        32: "밀레니얼 중반",
        37: "밀레니얼 초반"
    }
    return labels.get(age_group,"Z세대 후반")

# --- 세대별 연도 리스트 딕셔너리 추가 ---
AGE_GROUP_YEARS = {
    17: [2015, 2020, 2025],
    22: [2015, 2020, 2025],
    27: [2010, 2015, 2025],
    32: [2005, 2010, 2015, 2020, 2025],
    37: [2000, 2005, 2010, 2015, 2020, 2025],
}

# @app.get("/genre-change/")
# def genre_change_analysis(ageGroup: int = 17, startDt: str = '2024-01-01', endDt: str = '2025-03-31'):
#     external_api_url = 'https://data4library.kr/api/loanItemSrch'
#     api_key = get_secret("book_api_key")

#     # 날짜를 datetime으로 변환
#     try:
#         start_year = datetime.strptime(startDt, "%Y-%m-%d").year
#         end_year = datetime.strptime(endDt, "%Y-%m-%d").year
#     except ValueError:
#         raise HTTPException(status_code=400, detail="날짜 형식은 YYYY-MM-DD 여야 합니다")

#     # 캐싱 확인 (startDt, endDt를 캐시 키에 포함)
#     cached = get_cached_genre_analysis(ageGroup, startDt, endDt)
#     if cached:
#         return cached

#     # --- 연도 리스트를 AGE_GROUP_YEARS에서 직접 사용 ---
#     year_list = AGE_GROUP_YEARS.get(ageGroup, [])
#     results = []
#     from_age, to_age = get_age_range(ageGroup)
#     for year in year_list:
#         startDt_year = f"{year}-01-01"
#         endDt_year = f"{year}-12-31"
#         params = {
#             'authKey': api_key,
#             'startDt': startDt_year,
#             'endDt': endDt_year,
#             'from_age': str(from_age),
#             'to_age': str(to_age),
#             'format': 'json'
#         }
#         try:
#             res = requests.get(external_api_url, params=params)
#             res.raise_for_status()
#             api_data = res.json()
#             year_data = extract_top_book_info(api_data, year)
#             if year_data:
#                 results.append(year_data)
#         except Exception as e:
#             print(f"Error fetching data for {year}: {e}")
#         print(f"외부 API 요청 URL: {res.url}")

#     if not results:
#         raise HTTPException(status_code=404, detail="요청한 기간에 대한 데이터를 찾을 수 없습니다")

    # DataFrame으로 바로 변환
    # df = pd.DataFrame([{
    #     '연도': item.get('year') or item.get('연도'),
    #     '주제분류': item.get('classNm') or item.get('주제분류'),
    #     '대출수': item.get('topBook', {}).get('loanCount') if isinstance(item.get('topBook'), dict) else item.get('대출수'),
    # } for item in results])

    # # 모든 연도-장르 조합에 대해 0으로 채워서 pivot
    # years = sorted([int(y) for y in df['연도'].unique()])
    # genres = sorted(df['주제분류'].unique())
    # pivot = df.pivot(index='연도', columns='주제분류', values='대출수').reindex(index=years, columns=genres, fill_value=0)
    # datasets = []
    # for idx, genre in enumerate(genres):
    #     # NaN을 0으로 변환 후 int로 변환
    #     data_list = [int(x) if not pd.isna(x) else 0 for x in pivot[genre].tolist()]
    #     datasets.append({
    #         'label': genre,
    #         'data': data_list,
    #     })
    # chartjs_payload = {
    #     'labels': year_list,
    #     'datasets': datasets,
    #     'topBooks': [
    #         {
    #             "year": int(item.get('year') or item.get('연도')) if (item.get('year') or item.get('연도')) else None,
    #             "title": item.get('topBook', {}).get('title') if isinstance(item.get('topBook'), dict) else item.get('도서명'),
    #             "loanCount": int(item.get('topBook', {}).get('loanCount') if isinstance(item.get('topBook'), dict) else item.get('대출수')) if (item.get('topBook', {}).get('loanCount') if isinstance(item.get('topBook'), dict) else item.get('대출수')) else 0,
    #             "classNm": item.get('classNm') or item.get('주제분류'),
    #         }
    #         for item in results
    #     ]
    # }
    # save_genre_analysis(ageGroup, startDt, endDt, start_year, end_year, chartjs_payload)
    # return chartjs_payload

def get_generation_birth_range_by_age(age_group: int, 기준연도: int):
    # 세대별 나이 범위 (예시)
    age_ranges = {
        17: (17, 21),  # Z세대 후반
        22: (22, 26),  # Z세대 중심
        27: (27, 31),  # 밀레니얼 후반
        32: (32, 36),  # 밀레니얼 중반
        37: (37, 41),  # 밀레니얼 초반
    }
    from_age, to_age = age_ranges.get(age_group, (17, 21))
    from_birth = 기준연도 - to_age
    to_birth = 기준연도 - from_age
    return from_birth, to_birth

@app.get("/generation-genre-change/")
def generation_genre_change_analysis(ageGroup: int = 17, startDt: str = '2024-01-01', endDt: str = '2025-03-31', 기준연도: int = 2025):
    cached = get_cached_genre_analysis(ageGroup, startDt, endDt)
    if cached:
        return cached
    external_api_url = 'https://data4library.kr/api/loanItemSrch'
    api_key = get_secret("book_api_key")
    try:
        start_year = datetime.strptime(startDt, "%Y-%m-%d").year
        end_year = datetime.strptime(endDt, "%Y-%m-%d").year
    except ValueError:
        raise HTTPException(status_code=400, detail="날짜 형식은 YYYY-MM-DD 여야 합니다")

    from_birth, to_birth = get_generation_birth_range_by_age(ageGroup, 기준연도)
    year_list = list(range(start_year, end_year + 1))
    results = []
    for year in year_list:
        from_age = year - to_birth+1 # (예: 2015-2008=7)
        to_age = year - from_birth+1 # (예: 2015-2004=11)
        params = {
            'authKey': api_key,
            'startDt': f"{year}-01-01",
            'endDt': f"{year}-12-31",
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
            print(f"Error fetching generation data for {year}: {e}")
        print(f"외부 API 요청 URL: {res.url}")
        print("test")

    if not results:
        raise HTTPException(status_code=404, detail="요청한 기간에 대한 데이터를 찾을 수 없습니다")

    df = pd.DataFrame([{
        '연도': item.get('year') or item.get('연도'),
        '주제분류': item.get('classNm') or item.get('주제분류'),
        '대출수': item.get('topBook', {}).get('loanCount') if isinstance(item.get('topBook'), dict) else item.get('대출수'),
    } for item in results])

    # None 값을 'Unknown'으로 대체
    df['주제분류'] = df['주제분류'].fillna('Unknown')

    years = sorted([int(y) for y in df['연도'].unique()])
    genres = sorted(df['주제분류'].unique())
    pivot = df.pivot(index='연도', columns='주제분류', values='대출수').reindex(index=years, columns=genres, fill_value=0)
    datasets = []
    for idx, genre in enumerate(genres):
        data_list = [int(x) if not pd.isna(x) else 0 for x in pivot[genre].tolist()]
        datasets.append({
            'label': genre,
            'data': data_list,
        })
    chartjs_payload = {
        'labels': year_list,
        'datasets': datasets,
        'topBooks': [
            {
                "year": int(item.get('year') or item.get('연도')) if (item.get('year') or item.get('연도')) else None,
                "title": item.get('topBook', {}).get('title') if isinstance(item.get('topBook'), dict) else item.get('도서명'),
                "loanCount": int(item.get('topBook', {}).get('loanCount') if isinstance(item.get('topBook'), dict) else item.get('대출수')) if (item.get('topBook', {}).get('loanCount') if isinstance(item.get('topBook'), dict) else item.get('대출수')) else 0,
                "classNm": item.get('classNm') or item.get('주제분류'),
            }
            for item in results
        ]
    }
    save_genre_analysis(ageGroup, startDt, endDt, start_year, end_year, chartjs_payload)
    return chartjs_payload
