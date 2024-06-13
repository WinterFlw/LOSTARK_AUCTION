from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# JSON 파일 경로
json_file_path = 'data/extracted_data.json'

# JSON 파일에서 데이터 로드
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print("Loaded data:", data)  # 데이터 로드 확인용 출력
else:
    data = {"Items": []}
    print("No data found.")

@app.route('/')
def index():
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
