#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class RiskStatus(Enum):
    NOT_SUSPICIOUS = 'not_suspicious'
    SUSPICIOUS = 'suspicious'
    NOT_SUPPORT = 'not_support'
