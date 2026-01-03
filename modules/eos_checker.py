import requests
from datetime import datetime

class EoSChecker:
    def __init__(self):
        self.api_base = "https://endoflife.date/api"

    def get_eos_info(self, product_name, version):
        """
        제품명과 버전을 받아서 EoS 정보를 반환하는 함수
        Return: {
            'eol_date': '2025-12-31', 
            'status': 'Expired' | 'Warning' | 'Good', 
            'days_left': 120 (남은 일수)
        }
        """
        # 1. 제품명 소문자 변환 (API는 소문자만 받음: Nginx -> nginx)
        product_key = product_name.lower().strip()
        
        # Tomcat 같은 경우 'apache-tomcat'이 아니라 'tomcat'으로 호출해야 함
        if "tomcat" in product_key: product_key = "tomcat"
        
        url = f"{self.api_base}/{product_key}.json"
        
        try:
            # 2. API 호출
            response = requests.get(url)
            if response.status_code != 200:
                return {"status": "Unknown", "msg": "API 제품 데이터 없음"}
            
            cycles = response.json()
            
            # 3. 내 버전과 맞는 사이클 찾기
            # 예: 내 버전 "1.14.0" -> API 사이클 "1.14" 찾기
            target_cycle = None
            str_ver = str(version).strip()
            
            for cycle_data in cycles:
                cycle_ver = str(cycle_data['cycle']) # 예: "1.14"
                
                # 내 버전이 해당 사이클로 시작하면 매칭 (startswith)
                if str_ver.startswith(cycle_ver):
                    target_cycle = cycle_data
                    break
            
            if not target_cycle:
                return {"status": "Unknown", "msg": f"버전({str_ver}) 매칭 실패"}

            # 4. EoS 날짜 확인 및 계산
            eol = target_cycle.get('eol')
            
            if eol is False: # 아직 EoS 날짜가 안 정해짐 (최신 버전 등)
                return {"status": "Good", "eol_date": "Alive", "days_left": 9999}
            
            if isinstance(eol, str) and len(eol) >= 10:
                eol_date = datetime.strptime(eol, "%Y-%m-%d")
                today = datetime.now()
                days_left = (eol_date - today).days
                
                # 상태 판단 로직
                if days_left < 0:
                    status = "Expired"  # 이미 지남 (위험!)
                elif days_left < 365:
                    status = "Warning"  # 1년 미만 남음 (준비 필요)
                else:
                    status = "Good"     # 넉넉함
                    
                return {
                    "status": status,
                    "eol_date": eol,
                    "days_left": days_left
                }
            
            return {"status": "Unknown", "msg": "날짜 형식 오류"}

        except Exception as e:
            return {"status": "Error", "msg": str(e)}

# --- [단독 테스트용 코드] ---
# 이 파일을 직접 실행할 때만 작동함
if __name__ == "__main__":
    checker = EoSChecker()
    
    print("🧪 EoS 모듈 테스트 시작...\n")
    
    # 테스트 케이스
    test_data = [
        ("nginx", "1.14.0"),  # 옛날 버전 (이미 지났을 듯)
        ("nginx", "1.24.0"),  # 최신 버전
        ("tomcat", "8.5.27"), # 많이 쓰는 버전
        ("centos", "7")       # 곧 종료되는 OS
    ]
    
    for prod, ver in test_data:
        info = checker.get_eos_info(prod, ver)
        print(f"[{prod} {ver}] -> {info}")