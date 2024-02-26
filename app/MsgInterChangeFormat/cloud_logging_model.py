#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field

from shared.app.enums.cloud_logging_category_enum import CloudLoggingCategoryEnum
from shared.app.enums.cloud_logging_type_enum import CloudLoggingTypeEnum


class CloudLoggingModel(BaseModel):
    category: CloudLoggingCategoryEnum = Field(description="log 類別，例如 detect、event、exception")
    type: CloudLoggingTypeEnum = Field(description="log 類型，prediction、message、postback")
    detail: Optional[str] = Field(description="log 屬性細節，例如 start prediction、after prediction、receive message、send response")
    query_id: Optional[str] = Field(min_length=1, description="任務收到的 query_id，用於識別觸發 log 的事件")
    user_id: Optional[int] = Field(ge=0, description="任務發起人在資料庫中的 id")
    message_type: Optional[str] = Field(description="觸發 log 的輸入型態，例如 domain 或是 url")
    message_content: Optional[str] = Field(description="觸發 log 的輸入內容，例如 draw.io")
    action_name: Optional[str] = Field(None, description="新增代理紀錄")
    agent_name: str = Field(description="發出 log 的元件，例如 dispatch、fraud_detector")
    function_name: str = Field(description="發出 log 的 function name")
    content: Optional[dict] = Field(description="想夾帶的其他資訊，型態為 dict，例如 {user_message = 使用者簡訊內容}，如果沒有就留空")
    created_at: int = Field(ge=0, description="log 被拋出的時間")

    class Config:
        use_enum_values = True
