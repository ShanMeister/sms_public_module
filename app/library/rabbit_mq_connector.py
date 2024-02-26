#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pathlib
import sys
from contextlib import asynccontextmanager

import aio_pika.pool
from loguru import logger
from functools import partial

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from shared.app.MsgInterChangeFormat.mq_initial_parameter_format import MqInitialParameterFormat


class RabbitMQConnector:
    _instance = None
    _connection_pool = None

    def __new__(cls, mq_params: MqInitialParameterFormat):
        if cls._instance is None:
            cls._instance = super(RabbitMQConnector, cls).__new__(cls)
            try:
                # 使用 partial 函數確保 get_connection 在被呼叫時可以獲得正確的 mq_params，需要完整的傳入 self 以及參數
                cls._connection_pool = aio_pika.pool.Pool(
                    partial(cls.get_connection, cls._instance, mq_params),
                    max_size=mq_params.max_tasks,
                )
                logger.info("create connection to rabbit mq success")
            except Exception as error:
                logger.warning(f"connection to rabbit mq failed: {error}")
        return cls._instance

    async def get_connection(self, mq_params: MqInitialParameterFormat):
        logger.debug('get connection')
        return await aio_pika.connect_robust(
            host=mq_params.host_ip,
            port=mq_params.port,
            login=mq_params.login,
            password=mq_params.password,
            heartbeat=int(os.getenv('SCX_MQ_HEARTBEAT', 600))
        )
    @asynccontextmanager
    async def get_channel(self):
        logger.debug('get channel')
        async with self._connection_pool.acquire() as connection:
            channel = await connection.channel()
            yield channel  # 用 yield 代替 return

