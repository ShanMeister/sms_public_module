#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class CloudLoggingTypeEnum(Enum):
    PREDICTION = "prediction"
    MESSAGE = "message"
    POSTBACK = "postback"
