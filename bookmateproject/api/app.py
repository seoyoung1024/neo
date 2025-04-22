import requests, json
from fastapi import FastAPI, HTTPException
from datetime import datetime
from fastapi.staticfiles import StaticFiles
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib
import platform
import pymysql

plt.rcParams['font.family'] = 'NanumBarunGothic'

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

def get_cached_genre_analysis(age_group, start_year, end_year):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT result_json FROM genre_analysis
                WHERE age_group=%s AND start_year=%s AND end_year=%s
                ORDER BY created_at DESC LIMIT 1
            """
            cursor.execute(sql, (age_group, start_year, end_year))
            row = cursor.fetchone()
            if row:
                return json.loads(row["result_json"])
    finally:
        conn.close()
    return None

def save_genre_analysis(age_group, start_year, end_year, result_json):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO genre_analysis (age_group, start_year, end_year, result_json, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(sql, (
                age_group, start_year, end_year, json.dumps(result_json, ensure_ascii=False)
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
        22: (22, 26),  # MZ세대 초반
        27: (27, 31),  # 밀레니얼 세대 중반
        32: (32, 36),  # 밀레니얼 세대 후반
        37: (37, 41),  # X세대 초반
    }
    return age_ranges.get(age_group, (17, 21))

@app.get("/genre-change/")
def genre_change_analysis(ageGroup: int = 17, startDt: str = '2024-01-01', endDt: str = '2025-03-31'):
    external_api_url = 'https://data4library.kr/api/loanItemSrch'
    api_key = get_secret("book_api_key")

    # 날짜를 datetime으로 변환
    try:
        start_year = datetime.strptime(startDt, "%Y-%m-%d").year
        end_year = datetime.strptime(endDt, "%Y-%m-%d").year
    except ValueError:
        raise HTTPException(status_code=400, detail="날짜 형식은 YYYY-MM-DD 여야 합니다")

    img_path = os.path.join(static_dir, f"trend_{ageGroup}_{startDt}_{endDt}.png")

    # 캐싱: 이미지가 이미 있으면 바로 반환
    cached = get_cached_genre_analysis(ageGroup, start_year, end_year)
    if cached:
        return cached

    # 캐싱 확인
    if os.path.exists(img_path):
        # image_url 생성 방식 수정: static/ 경로를 /static/으로 변환
        if img_path.startswith("static/"):
            image_url = "/" + img_path  # /static/...
        else:
            image_url = img_path[img_path.find('/static/'):] if '/static/' in img_path else None
        # 데이터는 새로 받아서 반환 (동일 파라미터면 결과도 동일)
        results = []
        from_age, to_age = get_age_range(ageGroup)
        for year in range(start_year, end_year + 1):
            start = f"{year}-01-01"
            end = f"{year}-12-31"
            params = {
                'authKey': api_key,
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
        if not results:
            raise HTTPException(status_code=404, detail="요청한 기간에 대한 데이터를 찾을 수 없습니다")
        df = pd.DataFrame([{
            '연도': item.get('year') or item.get('연도'),
            '주제분류': item.get('classNm') or item.get('주제분류'),
            '도서명': item.get('topBook', {}).get('title') if isinstance(item.get('topBook'), dict) else item.get('도서명'),
            '대출수': item.get('topBook', {}).get('loanCount') if isinstance(item.get('topBook'), dict) else item.get('대출수'),
        } for item in results])
        df_json = df.to_dict(orient='records')
        result_json = {
            "graphImageUrl": image_url,
            "data": df_json
        }
        save_genre_analysis(ageGroup, start_year, end_year, result_json)
        return result_json

    # (이하 기존대로 외부 API 호출 → results → df → 그래프 생성)
    results = []
    from_age, to_age = get_age_range(ageGroup)
    for year in range(start_year, end_year + 1):
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        params = {
            'authKey': api_key,
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
        print(f"외부 API 요청 URL: {res.url}")

    if not results:
        raise HTTPException(status_code=404, detail="요청한 기간에 대한 데이터를 찾을 수 없습니다")

    # DataFrame으로 바로 변환
    df = pd.DataFrame([{
        '연도': item.get('year') or item.get('연도'),
        '주제분류': item.get('classNm') or item.get('주제분류'),
        '도서명': item.get('topBook', {}).get('title') if isinstance(item.get('topBook'), dict) else item.get('도서명'),
        '대출수': item.get('topBook', {}).get('loanCount') if isinstance(item.get('topBook'), dict) else item.get('대출수'),
    } for item in results])

    # 멀티라인 그래프 스타일 적용
    plt.figure(figsize=(8, 6))

    # 주제별 데이터 만들기
    pivot = df.pivot(index='연도', columns='주제분류', values='대출수').fillna(0)
    colors = ["#ff1919", "#ff9900", "#ffd700", "#1f77b4", "#2ca02c", "#9467bd"]
    label_color_map = {}
    # 범례 라벨을 단순화: 항상 두 번째 장르만 보이게
    def simplify_label(label):
        parts = [x.strip() for x in label.split('>')]
        if len(parts) >= 2:
            return parts[1]
        return parts[-1]
    simplified_labels = {col: simplify_label(col) for col in pivot.columns}

    for idx, col in enumerate(pivot.columns):
        label_color_map[col] = colors[idx % len(colors)]
        plt.plot(pivot.index, pivot[col], label=simplified_labels[col], color=label_color_map[col], linewidth=2)

    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=14, frameon=False)
    plt.title(f"{start_year}~{end_year}년도의{ageGroup}세\n독서 성향 분석 결과", fontsize=18, pad=30)
    plt.xlabel("")
    plt.ylabel("대출 수", fontsize=14, labelpad=15)
    plt.xticks(pivot.index, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', alpha=0.4)
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # 범례 공간 확보
    ax = plt.gca()
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.savefig(img_path, bbox_inches='tight')
    plt.close()
    # image_url 생성 방식 수정: static/ 경로를 /static/으로 변환
    if img_path.startswith("static/"):
        image_url = "/static/" + os.path.basename(img_path)
    else:
        image_url = img_path[img_path.find('/static/'):] if '/static/' in img_path else None

    # DataFrame을 JSON으로 반환
    df_json = df.to_dict(orient='records')

    result_json = {
        "graphImageUrl": image_url,
        "data": df_json
    }
    save_genre_analysis(ageGroup, start_year, end_year, result_json)
    return result_json

