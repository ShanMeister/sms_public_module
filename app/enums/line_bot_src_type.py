#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class LineBotSrcType(Enum):
    USER = "user"
    GROUP = "group"
    ROOM = "room"
    USER_ID = "user_id"
    GROUP_ID = "group_id"
    ROOM_ID = "room_id"
