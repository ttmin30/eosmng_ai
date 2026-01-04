import pandas as pd
import os

class AssetLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_assets(self):
        """
        엑셀 파일을 읽어서 두 가지 형태의 데이터를 반환함
        1. assets_dict_list (List[dict]): EoS 체크용 [{'name':..., 'version':...}]
        2. assets_str (str): AI 분석용 "- Name (Ver: ...)"
        """
        if not os.path.exists(self.file_path):
            return [], ""

        try:
            df = pd.read_excel(self.file_path, header=[1, 2])
            
            assets_dict_list = [] # ✅ [수정] EoS 체크를 위한 딕셔너리 리스트
            assets_str_list = []  # ✅ [수정] AI를 위한 문자열 리스트
            
            # 카테고리 순회
            for _, row in df.iterrows():
                for cat in ['OS', '미들웨어', '응용SW/DBMS']:
                    try:
                        name = str(row.get((cat, '종류'))).strip()
                        ver = str(row.get((cat, '버전'))).strip()
                        
                        if name not in ['nan', 'None'] and ver not in ['nan', 'None']:
                            # 1. 딕셔너리 저장 (Phase 1용)
                            assets_dict_list.append({"name": name, "version": ver})
                            
                            # 2. 문자열 저장 (Phase 2용)
                            assets_str_list.append(f"- {name} (Ver: {ver})")
                            
                    except: continue
            
            # 두 가지를 튜플로 반환
            return assets_dict_list, "\n".join(assets_str_list)

        except Exception as e:
            print(f"❌ 엑셀 로딩 실패: {e}")
            return [], ""