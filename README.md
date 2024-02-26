# sms-fraud-detect-line-bot-public-module
存放 sms fraud detection 的共用模組

# 專案目錄架構
```
.
├── app 主程式資料夾
│   ├── enums 程式運行時，列舉固定字串的 enum 檔案
├── storage 存放運行所需的檔案
│   ├── tests 系統整合測試所需的輸入資料
├── tests 測試相關檔案
│   ├── integration 系統整合測試，內含各個測試標的整合測試資料
├── README.md
```

# 測試執行方式
設定各自測試的環境設定檔

## integration test
1. 確認 tests 底下的 requirements.txt 有安裝
2. 複製 tests/integration/sms_fraud_detector/.env.example 為 tests/integration/sms_fraud_detector/.env 並補上設定空白值
3. 在專案根目錄下運行
    ```commandline
    pytest tests/integration/sms_fraud_detector/test_sms_fraud_detector_api.py
    ```
   若是需要整體限時，可加上 --timeout 秒數
4. 觀測結果
