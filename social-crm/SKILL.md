---
name: social-crm
description: "企業級社交與人脈資料庫管理技能 (Social CRM)。當使用者遇見新朋友、上傳別人的名片、截圖 (如 LinkedIn)、要查詢某位認識的朋友或大老闆背景，或詢問社交圈關係圖時啟動此技能。"
---

# 社交人脈庫 (Social CRM)

您的專屬人脈關係管理員，用來記錄名片、人臉、和互動細節。

## HARD GATE (反幻覺防呆條款)
- **絕對禁止捏造職稱與經歷**：只紀錄使用者提供的文字或圖片 (OCR) 內容。如果 OCR 失敗，請如實報告。
- **嚴格遵守資料結構**：請參考 `references/data-schema.md` 處理姓名、公司、背景等欄位格式。

## 執行 SOP (Multi-step Workflow)
1. **萃取資訊**：辨識使用者上傳的名片或對話，提取出「姓名」、「公司」、「職稱」、「背景」與「分類標籤」。
2. **特殊規則檢查**：閱讀 `references/data-schema.md` 中關於「扶輪社夫妻檔」與「聯絡人識別碼」的處理邏輯。
3. **智慧更新與建檔**：
   - 使用腳本：`uv run skills/social-crm/scripts/manage_contacts.py "<姓名>" "<公司/組織>" "<專長/職稱>" "<背景與過往經歷>" "<群組標籤>" "<照片路徑>"`
   - 參數帶入前，確保內容已遵循資料結構規範。
4. **回報更新狀態**：整理並條列出更新的欄位，以及附上「AI 人脈小分析」（例如該聯絡人對使用者的潛在價值或下次互動建議）。

## 查詢歷史紀錄
可以使用 pandas 讀取工作區的 `Social_Contacts.xlsx` 檔案來查詢。
或使用 `uv run skills/social-crm/scripts/find_contact.py "<姓名/關鍵字>"` 進行搜尋。
