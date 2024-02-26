#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 用於簡訊原文正規化的 decorator
def sms_text_normalize(func):
    def wrapper(self, text, *args, **kwargs):
        return func(self, text.lower(), *args, **kwargs)
    return wrapper
