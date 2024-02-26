#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class RiskLevel(Enum):
    UNKNOWN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    WELCOME = 95
    REACH_SYSTEM_USAGE_FREQUENCY_LIMIT = 96
    SYSTEM_IS_BUSY = 97
    THANKS_POSTBACK = 98
    NOT_SUPPORT = 99
