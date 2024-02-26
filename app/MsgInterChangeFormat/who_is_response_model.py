#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from datetime import datetime


class WhoisResponseModel(BaseModel):
    DomainName: str = Field(example='GOOGLE.COM')
    DomainUpdatedDate: datetime = Field(example='2019-09-09 15:39:04+00:00')
    DomainCreationDate: datetime = Field(example='1997-09-15 04:00:00+00:00')
    # 目前有兩種資料來源，分別是 whois.markmonitor.com 跟 data.iana.org
    datasource: str = Field(example='whois.markmonitor.com', description='whois資料來源')
