#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class UserFrequencyColumn(Enum):
    LAST_UPDATE_TIME = "last_update_time"
    SENT_EVENT_COUNT = "send_event_count"
