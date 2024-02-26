#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class LineResponseCategory(Enum):
    FRAUD_DETECTOR_TITLE = '詐騙訊息偵測結果'
    NOT_SUPPORT_TITLE = '當前未支援此類短訊偵測'
    POSTBACK_TITLE = '建議回饋結果'
    WELCOME_TITLE = '未知來源的簡訊讓人心驚驚？'
    SYSTEM_IS_BUSY = '系統忙碌中，請稍後再嘗試'
    REACH_SYSTEM_USAGE_FREQUENCY_LIMIT = '已達系統使用次數上限，請稍後再試'
