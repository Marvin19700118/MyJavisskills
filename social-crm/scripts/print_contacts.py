import pandas as pd
import sys
import json

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('Social_Contacts.xlsx')
print(json.dumps(json.loads(df.to_json(orient='records', force_ascii=False)), indent=2, ensure_ascii=False))