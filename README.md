# SnakeGame
python製作的貪食蛇遊戲專案

實作了帳號註冊、登入驗證、分數更新與查詢等功能。使用 JSON 作為資料儲存後端，搭配標準與第三方函式庫來處理密碼雜湊、路由設計等基礎
是一個後端開發學習的基礎專案

# 專案架構
.
├── auth.py        # 使用者註冊、登入與密碼驗證邏輯
├── main.py        # 提供 CLI 介面操作註冊、登入與查詢分數
├── users.json     # 儲存所有使用者帳號資訊
└── README.md      

# 功能特色
使用者註冊：帳號不得重複，自動將密碼加密後存入 JSON 檔案
使用者登入：支援鹽值加密驗證機制
分數更新：登入成功後可設定或查詢最高分數
資料儲存：以 users.json 作為簡單資料庫模擬

# 使用套件
hashlib
secrets
json
os

# 執行方式
確保環境已安裝 Python
將 auth.py, main.py, users.json 放在同一資料夾

執行主程式：python main.py

# future
加入 Flask/FastAPI，將認證邏輯包裝成 API。
改用 SQLite 儲存使用者與分數。
