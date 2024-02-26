#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from .wrapper_library import sms_text_normalize


class ExtractUrl:
    def __init__(self, tlds=None):
        # 如果未提供 TLD 列表，則使用預設值，提供後續彈性變動的可能性
        if tlds is None:
            tlds = ["com", "top", "vip", "xyz", "org", "icu", "support", "co", "gov", "id", "cc", "me", "ly", "info",
                    "ink", "click", "club", "buzz", "city", "wtf", "tw"]
        self.tld_pattern = "|".join(re.escape(tld) for tld in tlds)
        self.pattern_url = re.compile(r"https?://[^\s/$.?#].[^\s]*")
        self.pattern_domain = re.compile(r"([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+([^/]+)(.*))")
        # 新增先找出字串內有沒有 tld 後綴斜線的案例，若有，就表示這個輸入不需要補斜線
        self.pattern_tld_followed_by_slash = re.compile(r"(\.(?:{}))/".format(self.tld_pattern))
        self.pattern_slash = re.compile(r"(\.(?:{}))".format(self.tld_pattern))
        self.pattern_after_slash = re.compile(re.compile(r"(\.(?:{}))(/[A-Za-z0-9\-._~!$&'()*+,;=:@]+)".format(self.tld_pattern)))
        self.pattern_illegal_path = re.compile(r"(\.(?:{}))\/[.,]+".format(self.tld_pattern))
        # 用於過濾簡訊換行時截斷的 stx 字符
        self.pattern_stx = re.compile(r"[\x00-\x1F]")
        self.pattern_after_symbol = re.compile(r'[，。\s\n\t【】()].*')
        # 用於去除所有不應該出現在 url 內的字元
        self.pattern_banned_in_url_format = re.compile(r"[^a-zA-Z0-9-_.:/?#@!$&'()*+,;=]+")
        self.pattern_pure_char = re.compile(r"\S")
        self.pattern_chinese = re.compile(r"[\u4e00-\u9fff]+")

    # 把重複的邏輯包成 internal function，簡化程式架構
    def _match_url(self, text):
        # 由於後續 pattern 抓到換行會直接結束判斷，導致判斷結果失誤，且換行不應影響判斷結果，因此先行去除
        text = re.sub(r'\r?\n', '', text)
        match_url = re.search(self.pattern_url, text)
        if match_url:
            return match_url.group()
        return None
    
    def _match_domain(self, text):
        # 由於後續 pattern 抓到換行會直接結束判斷，導致判斷結果失誤，且換行不應影響判斷結果，因此先行去除
        text = re.sub(r'\r?\n', ' ', text)
        domain_match = re.search(self.pattern_domain, text)
        if domain_match:
            return domain_match.group()
        return None

    def _get_valid_uri(self, text):
        text_list = text.split(' ')
        for content in text_list:
            # 只有在內容包含 tld，且符合網域或 url 定義時，才回傳內容
            if (re.search(self.tld_pattern, content) and re.search(self.pattern_domain, content)) or re.search(self.pattern_url, content):
                return content
        # 否則就依照原有邏輯，通通兜在一起
        return ''.join(text_list)

    @sms_text_normalize
    def extract_urls(self, text: str):
        result_url = self._match_url(text)
        result_domain = self._match_domain(text)
        target_result = None
        if result_url is not None or result_domain is not None:
            target_result = result_url if result_url is not None else result_domain
            # 取代掉 stx 字符，還原簡訊
            target_result = re.sub(self.pattern_stx, '', target_result)
            target_result = re.sub(self.pattern_banned_in_url_format, " ", target_result)
            target_result = self._get_valid_uri(target_result)
            # step 1: 先找字串內有沒有 tld 後綴 / 的案例，以確認這個輸入需不需要補斜線做 uri 正規化
            tld_with_slash_matches = re.search(self.pattern_tld_followed_by_slash, text)
            if not tld_with_slash_matches:
                # step 2: 沒有任何 tld 後綴 /，開始列出所有 tld
                tld_matches = list(re.finditer(self.pattern_slash, target_result))
                if tld_matches:
                    # step 3: 如果有找到，就在最後一個 tld 後加上斜線，進行格式正規化
                    last_tld = tld_matches[-1]
                    target_result = target_result[:last_tld.end()] + "/" + target_result[last_tld.end():]
            target_result = re.sub(self.pattern_after_slash, lambda m: m.group(1) + m.group(2), target_result)
            target_result = re.sub(self.pattern_illegal_path, r"\1/", target_result)
            target_result = re.sub(self.pattern_after_symbol, '', target_result)
        return target_result

    @sms_text_normalize
    def has_url(self, text: str):
        return any([self._match_url(text), self._match_domain(text)])

    @sms_text_normalize
    def has_text_without_url(self, text: str):
        # 由於 line 本身若是 url 與其後的文字相連，本身就會被判斷為超連結，因此可一併移除
        no_urls = re.sub(self.pattern_url, '', text)
        # 由於上述規則僅判斷 url，若是簡訊中包含網域，也要納入判斷，如果去除了網域與 url 後還有純文字，才是要丟入後端的目標
        no_urls_and_domains = re.sub(self.pattern_domain, '', no_urls)

        # 因為擔心去除 url 後的文字，可能會有一些例外狀況，例如空白，所以用 search 跑結果，而不是用 len 做判斷
        return re.search(self.pattern_pure_char, no_urls_and_domains)


# 用於 singleton 呼叫的 object，因為這個 function 是相對穩定不易變動的，所以不用 IOC/DI 進行包裝
extractor = ExtractUrl()
