#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class SMSDetectorEnum(Enum):
    NEED_RELOAD_BANK_WHITELIST = 1
    NEED_RELOAD_TINYURL_WHITELIST = 2
    NEED_RELOAD_DOMAIN_WHITELIST = 3
    NEED_RELOAD_REGEX_LIST = 4
