#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field


class MqInitialParameterFormat(BaseModel):
    host_ip: str = Field(min_length=1)
    port: int = Field(gt=0)
    login: str = Field(min_length=1)
    # 應該不會有不設密碼的情況發生，所以也列為必填
    password: str = Field(min_length=1)
    queue_name: str = Field(min_length=1)
    max_tasks: int = 20
