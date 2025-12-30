import requests

def get_specific_eos(product_name, my_version):
    # 1. 일단 전체 족보(History)를 다 가져옴
    url = f"https://endoflife.date/api/{product_name}.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"오류: '{product_name}'이라는 제품을 찾을 수 없어."

    all_versions = response.json()

    my_ver_str = str(my_version)
    
    # 2. 반복문(Loop)을 돌면서 내 버전과 똑같은 게 있는지 찾음
    for item in all_versions:
        api_ver_str= str(item['cycle'])
        # item['cycle']은 API가 가진 버전 정보 (예: "20.04")
        # 문자열(str)로 변환해서 비교하는 게 안전함
        if my_ver_str == api_ver_str or my_ver_str.startswith(api_ver_str):
            return f"찾았다! {product_name} {my_version}의 EoS 날짜는 [{item['eol']}]야."
            
    return f"실패: {product_name} 목록에 {my_version} 버전은 안 보이는데?"

# --- 테스트 실행 ---

# 1. 성공 케이스 (Ubuntu 20.04)
print(get_specific_eos("ubuntu", "20.04"))

# 2. 성공 케이스 (Windows 10, 버전명을 '10'으로 줘야 함)
print(get_specific_eos("windows", "10"))

# 3. 실패 케이스 (없는 버전 넣어보기)
print(get_specific_eos("ubuntu", "99.99"))