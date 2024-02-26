#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class APIPathEnum(Enum):
    SMS_DETECTOR_URL_ENTRY = "sms_detector_url/detector"
    SMS_DETECTOR_ADDFRIEND_ENTRY = "sms_detector_addfriend/detector"
    API_KEY_NAME = "Authorization"
