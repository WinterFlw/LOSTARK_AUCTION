import requests, json, os
from dotenv import load_dotenv
import extract_fields as extr
import datetime

# load .env
load_dotenv()
API_KEY = os.environ.get('API_KEY')
AUCTION_ITEMS = os.environ.get('AUCTION_ITEMS')

# url은 검색 내용에 따라 변경해서 사용
url = AUCTION_ITEMS

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

#현재 찾고 싶은 아이템 이름.
item_name = "9레벨 멸화의 보석"

# 요청 본문 (API 문서에서 제공된 예제 값 사용)
data = {
  "Sort": "BUY_PRICE",
  "CategoryCode": 210000,
  "CharacterClass": None,
  "ItemTier": 3,
  "ItemGrade": "전설",
  "ItemName": item_name,
  "PageNo": 0,
  "SortCondition": "ASC"
}

# API 요청 보내기
response = requests.post(url, headers=headers, json=data)

# 응답 처리
if response.status_code == 200:
    response_data = response.json()
    # 받은 데이터를 .json 파일로 저장
    filename = datetime.datetime.now().strftime('%y%m%d%H%M')
    with open(f"data/raw_data/{filename}.json", "w", encoding="utf-8") as file:
        json.dump(response_data, file, ensure_ascii=False, indent=4)
    print(f"응답 데이터를 '{filename}.json' 파일로 저장했습니다.")
    
    # 데이터 가공하기
    fields_to_extract = ["Icon", "Name", "BuyPrice", "EndDate", "ClassName", "OptionName"]
    extracted_data = extr.extract_fields(response_data, fields_to_extract)
    extr.save_to_json(extracted_data, 'data/extracted_data.json')
    extr.plot_price_graph(extracted_data)
    print("가공 데이터 저장완료")
    
else:
    print(f"Error: {response.status_code}, Message: {response.text}")
