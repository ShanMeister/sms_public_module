#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class FraudDetectorPostbackEnum(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
