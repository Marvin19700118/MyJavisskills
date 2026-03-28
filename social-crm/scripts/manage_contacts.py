# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
#     "openpyxl"
# ]
# ///

import sys
import pandas as pd
from datetime import datetime
import os

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def create_or_update_contact(name, company, expertise, background, tags, photo_path):
    file_name = "Social_Contacts.xlsx"
    
    unique_id = f"{name} ({company})"
    
    new_data = pd.DataFrame([{
        "唯一識別碼": unique_id,
        "姓名": name,
        "公司/職稱": company,
        "專長": expertise,
        "過去經歷/背景": background,
        "朋友圈分類 (Tags)": tags,
        "照片特徵/路徑": photo_path,
        "最後互動日期": "尚未記錄",
        "下次聊天話題": "無"
    }])
    
    if os.path.exists(file_name):
        try:
            df = pd.read_excel(file_name)
            if unique_id in df['唯一識別碼'].values:
                idx = df.index[df['唯一識別碼'] == unique_id][0]
                df.loc[idx, '專長'] = expertise
                df.loc[idx, '過去經歷/背景'] = background
                df.loc[idx, '朋友圈分類 (Tags)'] = tags
                if photo_path != "無":
                    df.loc[idx, '照片特徵/路徑'] = photo_path
                print(f"成功更新現有聯絡人: {unique_id}")
            else:
                df = pd.concat([df, new_data], ignore_index=True)
                print(f"成功新增聯絡人: {unique_id}")
        except Exception as e:
            print(f"讀取舊檔案失敗: {e}")
            df = new_data
    else:
        df = new_data
        print(f"成功新增聯絡人: {unique_id}")
        
    df.to_excel(file_name, index=False)

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "未提供"
    company = sys.argv[2] if len(sys.argv) > 2 else "未提供"
    expertise = sys.argv[3] if len(sys.argv) > 3 else "未提供"
    bg = sys.argv[4] if len(sys.argv) > 4 else "未提供"
    tags = sys.argv[5] if len(sys.argv) > 5 else "未分類"
    photo = sys.argv[6] if len(sys.argv) > 6 else "無"
    
    create_or_update_contact(name, company, expertise, bg, tags, photo)