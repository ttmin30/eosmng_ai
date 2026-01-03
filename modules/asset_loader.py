import pandas as pd
import os

class AssetLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_assets(self):
        if not os.path.exists(self.file_path):
            return [], ""
        try:
            df = pd.read_excel(self.file_path, header=[1, 2])
            assets_str_list = []
            
            # 카테고리 순회
            for _, row in df.iterrows():
                for cat in ['OS', '미들웨어', '응용SW/DBMS']:
                    try:
                        name = str(row.get((cat, '종류'))).strip()
                        ver = str(row.get((cat, '버전'))).strip()
                        if name not in ['nan', 'None'] and ver not in ['nan', 'None']:
                            assets_str_list.append(f"- {name} (Ver: {ver})")
                    except: continue
            
            return assets_str_list, "\n".join(assets_str_list)
        except Exception as e:
            print(f"❌ 엑셀 로딩 실패: {e}")
            return [], ""