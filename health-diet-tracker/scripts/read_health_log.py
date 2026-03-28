# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
#     "openpyxl"
# ]
# ///

import sys
import pandas as pd
import json

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def read_log():
    file_name = "Health_Daily_Log.xlsx"
    try:
        df = pd.read_excel(file_name)
        result = df.to_json(orient="records", force_ascii=False)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    read_log()
