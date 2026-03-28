# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
#     "openpyxl"
# ]
# ///

import sys
import pandas as pd
import os
import json

def find_duplicates(name):
    file_name = "Social_Contacts.xlsx"
    if not os.path.exists(file_name):
        return json.dumps({"error": "找不到聯絡人資料庫 (Social_Contacts.xlsx)"}, ensure_ascii=False)
        
    try:
        df = pd.read_excel(file_name)
        # Filter rows where the name matches exactly
        matches = df[df['姓名'] == name]
        
        if matches.empty:
            return json.dumps({"status": "not_found", "message": f"找不到名為 {name} 的聯絡人。"}, ensure_ascii=False)
            
        results = []
        for index, row in matches.iterrows():
            results.append({
                "id": row['唯一識別碼'],
                "company": row['公司/職稱'],
                "expertise": row['專長'],
                "tags": row['朋友圈分類 (Tags)']
            })
            
        if len(results) == 1:
            return json.dumps({"status": "single_match", "data": results[0]}, ensure_ascii=False)
        else:
            return json.dumps({"status": "multiple_matches", "data": results}, ensure_ascii=False)
            
    except Exception as e:
        return json.dumps({"error": f"讀取檔案失敗: {e}"}, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "請提供要搜尋的姓名"}, ensure_ascii=False))
        sys.exit(1)
        
    search_name = sys.argv[1]
    print(find_duplicates(search_name))
