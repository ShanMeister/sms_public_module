#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class RedisPrefixEnum(Enum):
    CACHEABLE = "cacheable"
    PREDICT_RESULT = "predict_result"
    REPLY_TOKEN = "reply_token"
    WHOIS_RESULT = "whois_result"
