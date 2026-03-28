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

# Fix print encoding on Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def log_health(exercise, duration, notes, chatter, image_path, analysis_result):
    file_name = "Health_Daily_Log.xlsx"
    now = datetime.now()
    
    new_data = pd.DataFrame([{
        "日期": now.strftime("%Y-%m-%d"),
        "記錄時間": now.strftime("%H:%M:%S"),
        "運動項目": exercise,
        "持續時間": duration,
        "備註 (健康)": notes,
        "碎碎念 (日記)": chatter,
        "照片路徑": image_path,
        "AI 營養分析": analysis_result
    }])
    
    if os.path.exists(file_name):
        try:
            df = pd.read_excel(file_name)
            df = pd.concat([df, new_data], ignore_index=True)
        except Exception as e:
            print(f"讀取舊檔案失敗，將覆寫: {e}")
            df = new_data
    else:
        df = new_data
        
    df.to_excel(file_name, index=False)
    print(f"成功將新紀錄【附加】至 {file_name}")

if __name__ == "__main__":
    ex = sys.argv[1] if len(sys.argv) > 1 else "無"
    dur = sys.argv[2] if len(sys.argv) > 2 else "0"
    nts = sys.argv[3] if len(sys.argv) > 3 else "無"
    cht = sys.argv[4] if len(sys.argv) > 4 else "無"
    img = sys.argv[5] if len(sys.argv) > 5 else "無照片"
    ana = sys.argv[6] if len(sys.argv) > 6 else "無分析"
    
    log_health(ex, dur, nts, cht, img, ana)
