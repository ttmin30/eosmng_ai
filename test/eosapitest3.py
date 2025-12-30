from datetime import datetime
import requests

def get_smart_eos(product_name, my_version):
    url = f"https://endoflife.date/api/{product_name}.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None # 데이터 없음

    all_versions = response.json()
    
    # 내 버전(문자열)을 미리 만들어둠
    my_ver_str = str(my_version)

    for item in all_versions:
        api_ver_str = str(item['cycle'])
        
        # [핵심 로직]
        # 1. 완벽히 똑같거나 (==)
        # 2. 내 버전이 API 버전으로 시작하거나 (startswith)
        if my_ver_str == api_ver_str or my_ver_str.startswith(api_ver_str):
            return item['eol'] # 날짜만 쏙 반환
            
    return None # 못 찾음

def check_security_status(product_name, my_version):
    # 1. 위에서 만든 함수로 EoS 날짜 가져오기
    eos_date_str = get_smart_eos(product_name, my_version)
    
    print(f"[{product_name} {my_version}] 점검 결과:")
    
    # 2. 정보가 없는 경우
    if not eos_date_str:
        print("-> ⚠️ 정보 없음 (수동 확인 필요)")
        return

    # 3. EoS가 False인 경우 (아직 지원 종료일이 미정인 아주 최신 버전)
    if eos_date_str is False:
        print("-> 🟢 양호 (지원 종료 일정 없음)")
        return

    # 4. 날짜 계산 (여기가 핵심!)
    today = datetime.now()
    eos_date = datetime.strptime(eos_date_str, "%Y-%m-%d") # 문자열 -> 날짜 변환
    
    days_left = (eos_date - today).days # 남은 일수 계산

    # 5. 등급 판정
    print(f"-> EoS 날짜: {eos_date_str} (약 {days_left}일 남음)")
    
    if days_left < 0:
        print("-> 🔴 [심각] 지원 종료됨 (보안 취약점 노출 가능성 높음!)")
    elif days_left < 365:
        print("-> 🟠 [경고] 1년 이내 종료 (교체/업그레이드 계획 수립 필요)")
    else:
        print("-> 🟢 [양호] 지원 기간 넉넉함")
    print("-" * 30)

# --- 테스트 ---
check_security_status("ubuntu", "18.04.6") # 이미 지났을 걸?
check_security_status("ubuntu", "22.04")   # 아직 넉넉할 거고
check_security_status("windows", "10")     # 내년(2025)에 끝날 텐데?