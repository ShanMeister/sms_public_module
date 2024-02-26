#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import inspect

from google.cloud import logging as cloud_logging
from loguru import logger

from shared.app.MsgInterChangeFormat.cloud_logging_model import CloudLoggingModel
from shared.app.enums.cloud_logging_category_enum import CloudLoggingCategoryEnum
from shared.app.enums.cloud_logging_type_enum import CloudLoggingTypeEnum


class ProcessLog:
    def __init__(self, log_name: str):
        # 建立一個 local logger 實例，用於 cloud logger 因為各種因素無法連線時，本地端紀錄用途
        self.logger = logger
        try:
            self.cloud_logger = cloud_logging.Client().logger(log_name)
        except Exception as e:
            self.logger.warning(f"cloud logger create failed: {e}")

    def lb_log(self, agent_name, message_content=None, query_id=None, user_id=None, message_type=None, log_detail=None, log_level="INFO", content=None):
        try:
            # 取得呼叫此 function 的 function 名稱
            current_frame = inspect.currentframe()
            caller_frame = current_frame.f_back
            info = inspect.getframeinfo(caller_frame)

            message = CloudLoggingModel(
                category=CloudLoggingCategoryEnum.EVENT.value,
                type=CloudLoggingTypeEnum.MESSAGE.value,
                detail=log_detail,
                agent_name=agent_name,
                query_id=query_id,
                user_id=user_id,
                message_type=message_type,
                message_content=message_content,
                function_name=info.function,
                content=content or {},
                created_at=int(time.time()),
            ).dict()

            self._throw_cloud_logging(log_level, message)
        except Exception as error:
            logger.warning(f"throw log to cloud logging error: {error}")

    def _throw_cloud_logging(self, log_level, message):
        try:
            match log_level.lower():
                case "info":
                    self.cloud_logger.log_struct(message, severity='INFO')
                case "debug":
                    self.cloud_logger.log_struct(message, severity='DEBUG')
                case "notice":
                    self.cloud_logger.log_struct(message, severity='NOTICE')
                case "warning":
                    self.cloud_logger.log_struct(message, severity='WARNING')
                case "error":
                    self.cloud_logger.log_struct(message, severity='ERROR')
                case "critical":
                    self.cloud_logger.log_struct(message, severity='CRITICAL')
                case "alert":
                    self.cloud_logger.log_struct(message, severity='ALERT')
                case "emergency":
                    self.cloud_logger.log_struct(message, severity='EMERGENCY')
                case _:
                    raise Exception("unknown log level")
        except Exception as e:
            self.logger.warning(f"throw log to cloud logging failed: {e}")
            self.logger.debug(f"message: {message}")
