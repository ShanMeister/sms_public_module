#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import sys
import os
from pathlib import Path
# 把專案根目錄加到 sys.path 內，讓程式可以在根目錄下執行
from loguru import logger

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent.parent))

from tests.library.util import load_test_set_content
from app.library.extract_url import extractor

logger.remove()
logger.add("logs/test_{time:YYYY-MM-DD}.log", level=os.getenv('SCX_LOG_LEVEL', 'DEBUG'))


domain_data = load_test_set_content('./tests/unit/public/storage/domain_test_set.csv')


@pytest.mark.run(order=1)
@pytest.mark.parametrize("test_content", domain_data)
def test_normal_sms_api_endpoint(test_content):
    target_text = test_content['text']
    # 預期目標
    exp_url = test_content.get('extract_urls', '')
    exp_has_url = test_content.get('has_url', '')
    exp_has_text_without_url = test_content.get('has_text_without_url', '')

    # 測試內容
    url = extractor.extract_urls(target_text)
    has_url = int(bool(extractor.has_url(target_text)))
    has_text_without_url = int(bool(extractor.has_text_without_url(target_text)))
    assert url == exp_url, f"extract url failed, expected: {exp_url}, result: {url}"
    assert has_url == exp_has_url, f"has url failed, expected: {exp_has_url}, result: {has_url}"
    assert has_text_without_url == exp_has_text_without_url, f"has_text_without_url failed, expected: {exp_has_text_without_url}, result: {has_text_without_url}"
