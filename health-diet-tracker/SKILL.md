---
name: health-diet-tracker
description: "健康與飲食追蹤企業級技能。當使用者上傳食物照片、提到吃過什麼東西、回報運動紀錄，或查詢過去健康紀錄時啟動。具備反幻覺條款與專業的糖尿病飲食護欄。"
---

# 健康與飲食追蹤 (Health & Diet Tracker)

## HARD GATE (反幻覺防呆條款)
- **絕對禁止捏造食物**：若照片模糊或無法辨識，必須誠實回報「無法辨識照片內容，請重新上傳」，不允許瞎掰食物。
- **嚴格的醫學護欄**：提供之飲食建議必須依據 `references/diabetes-guidelines.md`，不可提供偏方或過度誇大效果。

## 執行 SOP (Multi-step Workflow)
1. **圖片與內容分析**：先辨識使用者提供的文字與照片內容，特別注意隱藏糖分與精緻澱粉。
2. **調閱專業指南**：參考 `references/diabetes-guidelines.md` 評估該餐點對糖尿病患者的優劣與 GI 值影響。
3. **建檔紀錄**：使用 `uv run skills/health-diet-tracker/scripts/log_health.py` 進行紀錄。
   - 參數：`<運動項目> <持續時間> <備註> <碎碎念> <照片路徑> <AI分析結果>`
   - 若無特定資訊，帶入 "無"。
4. **回報**：給予使用者明確的「優缺點分析」與「改善建議」（如剝掉麵衣、替換含糖飲料）。

## 查詢歷史紀錄
- 若使用者詢問過去紀錄，執行 `uv run skills/health-diet-tracker/scripts/read_health_log.py`，並進行重點摘要。
