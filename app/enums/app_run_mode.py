#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class AppRunMode(Enum):
    DEBUG = "debug"
    PRODUCTION = "production"
    TEST = "test"
