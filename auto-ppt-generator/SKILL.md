---
name: auto-ppt-generator
description: "企業級自動產生簡報技能。當使用者要求「幫我做一份簡報 (PPTX)」、「產生EMBA報告」、「製作記憶體產業報告」等需求時啟動。內建版面控制與專業格式產生器。"
---

# 簡報產生器 (PowerPoint Auto Generator)

一鍵快速產生結構化、專業的 PowerPoint 報告。

## 執行 SOP (Multi-step Workflow)
1. **主題確立與腳本選擇**：確認使用者所需的報告主題（如「AI 策略」、「記憶體產業」）。
2. **啟動生成器**：
   - 執行工作區 `skills/auto-ppt-generator/scripts/` 目錄下的相對應 Python 腳本。
   - `uv run skills/auto-ppt-generator/scripts/create_emba_pptx.py`
   - `uv run skills/auto-ppt-generator/scripts/create_90_pptx.py`
   - 如果需要客製化範本，請參考 `assets/` 目錄。
3. **回報成功狀態**：
   - 確認 `.pptx` 檔案是否生成在工作區。
   - 回傳訊息給使用者：「您的《[主題名稱]》簡報已經為您生成完畢！」並附上檔案名稱（如 `EMBA_AI_Strategy_Presentation.pptx`）。
   - 若使用者有後續修改需求，請提供編輯建議或直接利用 `python-pptx` 修改內容。