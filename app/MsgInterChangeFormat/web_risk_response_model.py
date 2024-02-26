#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field


class WebRiskModel(BaseModel):
    expire_time: str = Field(examples='2023-07-14 02:44:14.266525+00:00')
    is_safe_url: bool = Field(example=False)
    is_malware: bool = Field(example=False)
    is_social_engineering: bool = Field(example=False)
    is_unwanted_software: bool = Field(example=False)
    is_social_engineering_extended_coverage: bool = Field(example=False)
