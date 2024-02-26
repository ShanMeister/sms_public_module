#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class RiskMessage(Enum):
    NO_URL = '目前尚無法判定是否為詐騙訊息。若您覺得可疑請通報，共同打擊詐騙，幫助更多人!'
    UNKNOWN = '目前尚無法判定是否為詐騙訊息。若您覺得可疑請通報，共同打擊詐騙，幫助更多人!'
    LOW = '目前尚無法判定是否為詐騙訊息。若您覺得可疑請通報，共同打擊詐騙，幫助更多人!'
    MEDIUM = '覺得我們誤判，或是此訊息真的很可疑? 請點下方通報選項，幫助更多人!'
    HIGH = '覺得我們誤判，或是此訊息真的很可疑? 請點下方通報選項，幫助更多人!'
    NOT_SUSPICIOUS = '此簡訊內容尚未有人回報'
    SUSPICIOUS_URL = '內容含不安全的URL網址'
    SUSPICIOUS_ADDFRIEND = '加好友前請確認對方身分'
    MISJUDGE = '回報疑似誤報'
    FRAUD = '回報疑似詐騙簡訊'
    PREDICT_NOT_SUSPICIOUS = '目前未於我們的資料庫中，找到與您所提供的訊息相匹配之資訊，若您仍然覺得可疑或確定本則為詐騙訊息，可點擊下方「回報疑似詐騙」進行回報，幫助更多人。'
    PREDICT_URL_SUSPICIOUS = '您輸入的內容可能有詐騙意圖，請保持警惕！若您確認此為誤報，請點擊下方按鈕回報，讓我們有改善的機會。'
    PREDICT_LINE_SUSPICIOUS = '許多詐騙集團會假裝成您久違的朋友，或用不合理的低利貸款、超高投資報酬率來誘使您加他為好友，接著進行下一階段的詐騙，請務必提高警覺！若您確認此為誤報，請點擊下方按鈕回報，讓我們有改善的機會。'
    THANKS_POSTBACK = '感謝您的回報'
    THANKS_POSTBACK_MESSAGE = '我們會盡速針對您的建議進行評估改善。'
    NOT_SUPPORT = '暫不支援此內容'
    INSUFFICIENT_INFO = '防詐隊長需要更多資訊'
    NOT_SUPPORT_WITHOUT_URL = '目前防詐隊長僅會針對 “含有網址“ 及 “要求加 Line 好友“ 類型的訊息進行分析喔。'
    NOT_SUPPORT_ONLY_URL = '請輸入包含文字內容及可疑網址的完整簡訊，防詐隊長才能更精確地為您分析唷。'
    SYSTEM_IS_BUSY = '目前查詢人數眾多，請稍後再嘗試'
    REACH_SYSTEM_USAGE_FREQUENCY_LIMIT = '⚠️請稍後再試⚠️'
    REACH_SYSTEM_USAGE_FREQUENCY_LIMIT_CONTENT = '已達系統使用次數上限，請稍後再試。'
    WELCOME_TITLE = '您的網路安全好夥伴'
    WELCOME_CONTENT = """
    ✔ 若您收到來源不明或是可疑的簡訊，請直接把整則簡訊複製貼到對話中，交由防詐隊長替您把關！
    ✔ 防詐隊長完全遵守LINE相關規範，不會也無法收集使用者的個人資料。
    ✔ 目前防詐隊長僅支援查詢 “含有網址“ 及 “要求加 Line 好友“ 之簡訊，後續會再努力優化偵測功能，敬請期待。
    """
    DOWNLOAD_SERVICE_DOCUMENT_FILE = '下載服務條款及隱私政策'
