#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class WebHookCategory(Enum):
    FRAUD_DETECTOR = "fraud_detector"
    FD_POSTBACK = "FD_postback"
    DISPATCH_FOLLOW = "dispatch_follow"
