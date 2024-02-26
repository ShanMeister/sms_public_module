#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field, validator
from datetime import datetime
from uuid import UUID
from typing import Union

from shared.app.MsgInterChangeFormat.webhook_dispatch_communication import SentryModel
from shared.app.MsgInterChangeFormat.who_is_response_model import WhoisResponseModel


class FDRequestModel(BaseModel):
    QueryId: str = Field(example="123e4567-e89b-12d3-a456-426655440000")
    QueryType: str = Field(min_length=1, example="sms_fraud")
    QueryBody: str = Field(min_length=1, example="你台X信用卡卡費已逾期請速至 https:\/\/fraud.com&nbsp;繳納")
    QueryDateTime: datetime = Field(example="2023-05-22T13:20:41.612Z")
    Sentry: Optional[SentryModel]


class ExpertSystemModel(BaseModel):
    Official: Optional[int] = Field(ge=0, le=1, example=0, description="This field can be 0, 1, or None")
    Whitelist: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")
    Regex: Optional[int] = Field(ge=0, le=1, example=None, description="This field can be 0, 1, or None")


class UrlBasedFeatureModel(BaseModel):
    TinyUrl: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")
    IsUrlRedirect: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")
    IsFreshDomain: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")
    IsShortUpdateRange: Optional[int] = Field(ge=0, le=1, example=0, description="This field can be 0, 1, or None")


class TextBasedFeatureModel(BaseModel):
    HasFraudText: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")


class CategoryModel(BaseModel):
    category: Optional[str] = Field(example='other', description="This field can be other, loan, investment, pretence, free, market or None")


class PatternModel(BaseModel):
    pattern: float = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")


class IntentionModel(BaseModel):
    urgency: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")
    enticement: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")
    alluring: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")
    tempting: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")
    irresistible: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")
    familiar: Optional[int] = Field(ge=0, le=1, example=1, description="This field can be 0, 1, or None")


class SMSDetectorURLModel(BaseModel):
    Probability: float = Field(ge=0.0, le=1.0, example=0.75)
    Url: str = Field(min_length=1, example="draw.io")
    Cacheable: bool = Field(example=True)
    ExpertSystem: ExpertSystemModel
    UrlBasedFeature: UrlBasedFeatureModel
    TextBasedFeature: TextBasedFeatureModel


class SMSDetectorAddFriendModel(BaseModel):
    Probability: float = Field(ge=0.0, le=1.0, example=0.75)
    SMSCategory: CategoryModel
    SMSPattern: PatternModel
    SMSIntention: IntentionModel


class FDResponseBodyModel(BaseModel):
    type: str
    SMSDetector: Union[SMSDetectorURLModel, SMSDetectorAddFriendModel]

    @validator("SMSDetector", pre=True, always=True)
    def validate_data(cls, value, values):
        # 在這裡根據 data 的內容進行判斷
        data_type = values.get('type')

        if data_type == 'line':
            return SMSDetectorAddFriendModel(**value)
        elif data_type == 'url':
            return SMSDetectorURLModel(**value)
        else:
            raise ValueError("Invalid data type")


class FDResponseModel(BaseModel):
    QueryId: str = Field(example="123e4567-e89b-12d3-a456-426655440000")
    ResponseId: UUID = Field(example="9ace45dd-e555-eed3-ca56-632655440132")
    ResponseMessage: str = Field(example="Success")
    ResponseBody: FDResponseBodyModel
    ResponseDateTime: datetime = Field(example="2023-05-22T13:24:11.031Z")


class FDReferRequestModel(BaseModel):
    QueryId: str = Field(example="123e4567-e89b-12d3-a456-426655440000")
    Domain: str = Field(min_length=1, example="google.com")


class FDReferResponseModel(BaseModel):
    QueryId: str = Field(example="123e4567-e89b-12d3-a456-426655440000")
    result: Optional[WhoisResponseModel] = Field(description="這個欄位若為空，表示完全沒有資料")
