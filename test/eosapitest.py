import requests
import json

def test_eos_api(product_name):
    print(f"--- [{product_name}] 검색 시작 ---")
    
    # 1. API 주소 만들기 (소문자, 띄어쓰기 대신 하이픈)
    url = f"https://endoflife.date/api/{product_name}.json"
    
    # 2. 데이터 요청
    response = requests.get(url)
    
    # 3. 결과 확인
    if response.status_code == 200:
        data = response.json()
        
        # 데이터가 너무 많을 수 있으니 최신 2개 버전만 출력해서 눈으로 확인
        print(f"✅ 데이터 수신 성공! (총 {len(data)}개의 버전 정보가 있습니다.)")
        print("\n[최신 버전 데이터 샘플]")
        
        # 보기 좋게 출력 (JSON Pretty Print)
        print(json.dumps(data[:2], indent=4, ensure_ascii=False)) 
        
    else:
        print(f"❌ 실패! '{product_name}'이라는 제품을 찾을 수 없습니다.")
        print("팁: 정확한 영문 명칭(예: windows, ubuntu, python)을 써야 합니다.")
    
    print("-" * 30 + "\n")

# --- 여기서 직접 테스트 해보게 ---
# 1. 리눅스 대표주자 Ubuntu
test_eos_api("ubuntu")

# 2. 윈도우 (Windows)
test_eos_api("windows")

# 3. 없는 이름 넣어보기 (오류 확인용)
test_eos_api("korea-software")