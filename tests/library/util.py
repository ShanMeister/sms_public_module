#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import os.path
import random
import pandas as pd


def generate_random_string(count: int):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=count))


def get_target_key_in_dict(input_dict: dict, key_str: str, excluded_key=None):
    keys = key_str.split('.')
    result = input_dict.copy()
    for key in keys:
        result = result.get(key, result)
        if isinstance(result, list) and excluded_key is not None:
            temp = result[0]
            if excluded_key not in temp:
                break
            else:
                result = result[0]
    return result


def generate_signature_by_content(channel_secret: str, content: str):
    hash_obj = hmac.new(
        bytes(channel_secret, 'latin-1'),
        msg=bytes(content, 'latin-1'),
        digestmod=hashlib.sha256
    )
    return base64.b64encode(hash_obj.digest()).decode('utf-8')


def load_test_set_content(file_path: str):
    if not os.path.exists(file_path):
        raise Exception('test set file not exist')
    data = pd.read_csv(file_path)
    data = data.where(data.notnull(), None)
    dict_data = data.to_dict('records')
    return dict_data
