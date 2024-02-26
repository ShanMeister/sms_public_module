#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field


class EventMessageModel(BaseModel):
    Type: str = Field(min_length=1, max_length=16, example="text")
    Id: str = Field(min_length=1, max_length=100, example="14353798921116")
    Text: str = Field(example="Hello")


class EventSourceModel(BaseModel):
    Type: str = Field(min_length=1, max_length=16, example="text")
    # 此處模型設定為 line platform 對 message 的來源格式驗證宣告，例如來源為 user，就會是 Type=user, UserId=Ub33dcbd5a06fb0af2f1b8c7808682bde
    # 但於 v1.0.1 上線時，發現 line platform 對於 API 的格式有異動，例如邀請使用者加入群組時，原格式為 Type=group, GroupId=Cb1241808a899e0dc885cf0d1929cd515
    # 會有發生回傳格式變成 Type=group, GroupId=Cb1241808a899e0dc885cf0d1929cd515, UserId=None 的狀況
    # 因此格式驗證加上預設值，即使 line platform 有給予欄位但沒有給值，也可以正常接受 line platform 給的 message request
    # 而格式合理性的正確與否，會在各模組 implement 時的 data validation 階段進行驗證
    UserId: Optional[str] = Field(None, min_length=1, max_length=64, example="Ub33dcbd5a06fb0af2f1b8c7808682bde")
    GroupId: Optional[str] = Field(None, min_length=1, max_length=64, example="Cb1241808a899e0dc885cf0d1929cd515", description="this column can be string or None")
    RoomId: Optional[str] = Field(None, min_length=1, max_length=64,  example="Cb1241808a899e0dc885cf0d1929cd515", description="this column can be string or None")


class SentryModel(BaseModel):
    TraceId: Optional[str] = Field(min_length=1, example="14b2e443e97e4e399e7d2b2c6a0eee2d")
    SpanId: Optional[str] = Field(min_length=1, example="aef45e9119e3a592")
    Op: Optional[str] = Field(min_length=1, example="task")
    Description: Optional[str] = Field(min_length=1, example="line bot task 2023-07-26 12:07")


class WebHookLineMessageEventModel(BaseModel):
    Target: str = Field(min_length=1, max_length=32, example="fraud_detector")
    Type: str = Field(min_length=1, max_length=32, example="message")
    ReplyToken: str = Field(min_length=1, max_length=100, example="4491918c330f4e5fa685cbfc1730a6b6")
    WebHookEventId: str = Field(min_length=1, max_length=100, example="01FZ74A0TDDPYRVKNK77XKC3ZR")
    Timestamp: int = Field(example=1689141467)
    Source: EventSourceModel
    Message: EventMessageModel
    Sentry: Optional[SentryModel]


class WebHookLinePostbackEventModel(BaseModel):
    Target: str = Field(min_length=1, max_length=32, example="postback")
    Type: str = Field(min_length=1, max_length=32, example="postback")
    ReplyToken: str = Field(min_length=1, max_length=100, example="b9d4fd88535e42f7a8b2770842952fa7")
    WebHookEventId: str = Field(min_length=1, max_length=100, example="01H5SJSKF9N7KMBAJ0JP7B7Y1W")
    Timestamp: int = Field(example=1689854462963)
    Data: str = Field(min_length=1, max_length=100, example="report=positive&event=01H5SB6X3KEFFSJCJX5FVXMXA1")
    Source: EventSourceModel
    Sentry: Optional[SentryModel]


class WebHookLineFollowEventModel(BaseModel):
    Target: str = Field(min_length=1, max_length=32, example="dispatch_follow")
    Type: str = Field(min_length=1, max_length=32, example="follow")
    ReplyToken: str = Field(min_length=1, max_length=100, example="4491918c330f4e5fa685cbfc1730a6b6")
    WebHookEventId: str = Field(min_length=1, max_length=100, example="01FZ74A0TDDPYRVKNK77XKC3ZR")
    Timestamp: int = Field(example=1689141467)
    Source: EventSourceModel
    Sentry: Optional[SentryModel]
