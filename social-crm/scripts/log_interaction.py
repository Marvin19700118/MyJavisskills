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

def log_interaction(name, interaction_notes, future_topic):
    file_name = "Social_Interactions_Log.xlsx"
    now = datetime.now()
    
    new_data = pd.DataFrame([{
        "日期": now.strftime("%Y-%m-%d"),
        "對象姓名": name,
        "本次互動重點摘要": interaction_notes,
        "建議的下次聊天話題": future_topic
    }])
    
    if os.path.exists(file_name):
        try:
            df = pd.read_excel(file_name)
            df = pd.concat([df, new_data], ignore_index=True)
        except Exception as e:
            print(f"讀取舊檔案失敗: {e}")
            df = new_data
    else:
        df = new_data
        
    df.to_excel(file_name, index=False)
    print(f"成功儲存互動紀錄至 {file_name}")
    
    contact_file = "Social_Contacts.xlsx"
    if os.path.exists(contact_file):
        cdf = pd.read_excel(contact_file)
        if name in cdf['姓名'].values:
            idx = cdf.index[cdf['姓名'] == name][0]
            cdf.loc[idx, '最後互動日期'] = now.strftime("%Y-%m-%d")
            cdf.loc[idx, '下次聊天話題'] = future_topic
            cdf.to_excel(contact_file, index=False)
            print(f"同步更新 {contact_file} 的最後互動日期與下次話題。")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "未知對象"
    notes = sys.argv[2] if len(sys.argv) > 2 else "無互動內容"
    topic = sys.argv[3] if len(sys.argv) > 3 else "無建議話題"
    
    log_interaction(name, notes, topic)
