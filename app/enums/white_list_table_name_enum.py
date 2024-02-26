#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class WhiteListTableNameEnum(Enum):
    BANK_WHITELISTS = "bank_whitelists"
    DOMAIN_WHITELISTS = "domain_whitelists"
    TINY_URL_WHITELISTS = "tiny_url_whitelists"
    REGEX_LISTS = "regex_lists"
