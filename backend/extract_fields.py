import json
import os
import matplotlib.pyplot as plt
def extract_fields(data, fields):
    """
    JSON 데이터에서 특정 필드를 추출하는 함수

    Args:
    - data (dict): 추출할 데이터가 포함된 JSON 형식의 딕셔너리
    - fields (list): 추출할 필드 이름이 포함된 리스트

    Returns:
    - list: 추출된 데이터를 담은 리스트
    """
    extracted_data = []

    for item in data["Items"]:
        new_item = {}
        for field in fields:
            if field in item["AuctionInfo"]:
                new_item[field] = item["AuctionInfo"][field]
            elif field == "ClassName" or field == "OptionName":
                if item["Options"]:
                    new_item[field] = item["Options"][0][field]
                else:
                    new_item[field] = None
            else:
                new_item[field] = item.get(field)
        extracted_data.append(new_item)

    return extracted_data

def save_to_json(data, filename):
    """
    JSON 형식의 데이터를 파일에 저장하는 함수(파일이 있다면 이어쓰기, 중복 데이터는 제외)

    Args:
    - data (list): 저장할 데이터가 담긴 리스트
    - filename (str): 저장할 파일의 경로 및 이름
    """
    # 파일이 존재하면 기존 데이터를 읽어온다.
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # 기존 데이터와 새 데이터를 합친다.
    combined_data = existing_data + data

    # 중복을 제거하기 위해 dict를 사용하여 고유한 항목만 남긴다.
    unique_data = {json.dumps(item, ensure_ascii=False): item for item in combined_data}.values()

    # 중복 제거 후 리스트로 변환
    unique_data_list = list(unique_data)

    # 데이터를 파일에 저장한다.
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(unique_data_list, f, ensure_ascii=False, indent=4)

def plot_price_graph(data):
    """
    데이터에서 가격과 종료 일자를 추출하여 그래프를 생성하고 이미지 파일로 저장하는 함수
    """
    prices = [item['BuyPrice'] for item in data]
    end_dates = [item['EndDate'][:10] for item in data]

    plt.figure(figsize=(10, 5))
    plt.plot(end_dates, prices, marker='o')
    plt.xlabel('End Date')
    plt.ylabel('Price')
    plt.title('Price Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()

    graph_path = 'static/price_graph.png'
    plt.savefig(graph_path)
    plt.close()
    