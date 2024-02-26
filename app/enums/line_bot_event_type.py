#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class LineBotEventType(Enum):
    MESSAGE = "message"
    POSTBACK = "postback"
    FOLLOW = "follow"
    JOIN = "join"
