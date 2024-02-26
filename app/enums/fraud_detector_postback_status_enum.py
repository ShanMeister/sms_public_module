#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class FraudDetectorPostbackStatusEnum(Enum):
    INVALID_DATA_FORMAT = "invalid_data_format"
    PARSE_DATA_ERROR = "parse_data_error"
    EVENT_NOT_EXIST = "event_not_exist"
    UNAUTHORIZED = "unauthorized"
    ALREADY_POSTED = "already_posted"
    INVALID_STATUS = "invalid_status"
    MYSQL_VALIDATION_FAILED = "mysql_validation_failed"
    SUCCESS_POSTED = "success_posted"
    PARSE_POSTBACK_STATUS_FAILED = "parse_postback_status_failed"
