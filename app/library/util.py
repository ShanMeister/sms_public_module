#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.util import strtobool

def convert_all_to_str(obj):
    if isinstance(obj, dict):
        # If the object is a dictionary, recursively convert its values
        return {k: convert_all_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # If the object is a list, recursively convert its elements
        return [convert_all_to_str(e) for e in obj]
    else:
        # Otherwise, convert the object to a string
        return str(obj)


def load_bool_from_env(key: str):
    return bool(strtobool(os.getenv(key)))
