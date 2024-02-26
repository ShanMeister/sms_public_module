#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import os

import redis
from loguru import logger
from redis.connection import SSLConnection

from shared.app.MsgInterChangeFormat.web_risk_response_model import WebRiskModel
from shared.app.MsgInterChangeFormat.who_is_response_model import WhoisResponseModel
from shared.app.enums.redis_prefix_enum import RedisPrefixEnum
from shared.app.enums.user_frequency_category import UserFrequencyCategory
from shared.app.enums.user_frequency_column import UserFrequencyColumn
from shared.app.enums.white_list_status_enum import WhiteListStatusEnum
from shared.app.enums.white_list_table_name_enum import WhiteListTableNameEnum
from shared.app.enums.who_is_source_category import WhoIsSourceCategory


class RedisImplement:
    def __init__(self):
        self.account = os.getenv('SCX_REDIS_ACCOUNT')
        self.host = os.getenv('SCX_REDIS_HOST')
        self.port = int(os.getenv('SCX_REDIS_PORT'))
        self.max_conn = int(os.getenv('SCX_REDIS_MAX_CONNECTION'))
        self.reply_token_timeout = int(os.getenv('SCX_REDIS_REPLY_TOKEN_TIMEOUT'))
        self.predict_result_timeout = int(os.getenv('SCX_REDIS_PREDICT_RESULT_TIMEOUT'))
        self.webrisk_response_timeout = int(os.getenv('SCX_REDIS_WEBRISK_RESPONSE_TIMEOUT'))
        self.who_is_response_timeout = int(os.getenv('SCX_REDIS_WHOIS_RESPONSE_TIMEOUT'))
        self.predict_missing_timeout = int(os.getenv('SCX_REDIS_PREDICT_MISSING_TIMEOUT'))
        self.cert_enabled = os.getenv('REDIS_REQUIRED_SSL') == 'True'
        self.ssl_ca_file = os.getenv('REDIS_SSL_CA_FILE')
        self.conn = None

        logger.debug(f"ssl enable: {self.cert_enabled}")

        if not os.path.exists(self.ssl_ca_file):
            logger.warning(f"cert file on path: {self.ssl_ca_file} not exist")

        try:
            connection_args = {
                'host': self.host,
                'port': self.port,
                'max_connections': self.max_conn,
                'password': os.getenv('SCX_REDIS_PASSWORD')
            }

            # 如果帳號有值，就採用 ACL 登入，反之則用預設權限登入
            if self.account:
                logger.debug(f"ACL enables, login with: {self.account}")
                connection_args.update({
                    'username': self.account
                })

            # 如果要啟用 ssl，就登記 connection_class 相關訊息
            if self.cert_enabled:
                logger.debug(f"cert enabled: {self.cert_enabled}, {os.getenv('REDIS_REQUIRED_SSL')}")
                connection_args.update({
                    'connection_class': SSLConnection,
                    'ssl_ca_certs': self.ssl_ca_file,
                })

            pool = redis.ConnectionPool(**connection_args)
            self.conn = redis.Redis(connection_pool=pool)
            logger.info("connection to redis success")
        except Exception as e:
            logger.warning(f"connection to redis failed: {e}")

    def get_message_predict_result(self, message: str):
        # 把輸入的訊息轉成 hash，再取得 redis 內的資料
        message_hash = hashlib.sha256(f"{RedisPrefixEnum.PREDICT_RESULT.value}-{message}".encode('utf-8')).hexdigest()
        result = self.conn.get(message_hash)
        return float(result) if result is not None else result

    def set_reply_token(self, query_id: str, reply_token: str):
        # 把輸入的 query_id 轉成 hash，再存入 redis
        query_id_hash = hashlib.sha256(f"{RedisPrefixEnum.REPLY_TOKEN.value}-{query_id}".encode('utf-8')).hexdigest()
        self.conn.set(query_id_hash, reply_token, ex=self.reply_token_timeout)

    def set_message_predict_result(self, message: str, predict_result):
        # 把輸入的 query_id 轉成 hash，再存入 redis
        message_hash = hashlib.sha256(f"{RedisPrefixEnum.PREDICT_RESULT.value}-{message}".encode('utf-8')).hexdigest()
        self.conn.set(message_hash, predict_result, ex=self.predict_result_timeout)

    def set_webrisk_response(self, uri: str, web_risk_response: WebRiskModel):
        # 把輸入的 query_id 轉成 hash，再存入 redis
        uri_hash = hashlib.sha256(uri.encode('utf-8')).hexdigest()
        logger.info(f"uri hash: {uri_hash}")
        self.conn.set(uri_hash, web_risk_response.json(), ex=self.webrisk_response_timeout)

    def set_who_is_response(self, domain: str, who_is_response: WhoisResponseModel):
        # 把輸入的 query_id 轉成 hash，再存入 redis
        domain_hash = hashlib.sha256(f"{RedisPrefixEnum.WHOIS_RESULT.value}-{domain}".encode('utf-8')).hexdigest()
        logger.info(f"domain hash: {domain_hash}, {who_is_response}")
        self.conn.hset(domain_hash, who_is_response.datasource, who_is_response.json())
        self.conn.expire(domain_hash, self.who_is_response_timeout)

    def get_who_is_response(self, domain: str):
        # 把輸入的 query_id 轉成 hash，再從 redis 取值
        domain_hash = hashlib.sha256(f"{RedisPrefixEnum.WHOIS_RESULT.value}-{domain}".encode('utf-8')).hexdigest()
        logger.info(f"domain hash: {domain_hash}")
        who_is_source_list = [member.value for member in WhoIsSourceCategory.__members__.values()]
        return self.conn.hmget(domain_hash, who_is_source_list)

    def set_predict_missing_times(self, message: str, count: int):
        # 把輸入的訊息加上 prefix，標駐是不可 cache 的內容，與原本的 key 值做分別，再進行 hash 與存入 redis
        message_hash = hashlib.sha256(f"{RedisPrefixEnum.CACHEABLE.value}-{message}".encode('utf-8')).hexdigest()
        self.conn.set(message_hash, count, ex=self.predict_missing_timeout)

    def get_predict_missing_result(self, message: str):
        # 把輸入的訊息加上 prefix，標駐是不可 cache 的內容，再進行 hash 與取得 redis 內的資料
        message_hash = hashlib.sha256(f"{RedisPrefixEnum.CACHEABLE.value}-{message}".encode('utf-8')).hexdigest()
        result = self.conn.get(message_hash)
        return float(result) if result is not None else result

    def set_fraud_update_whitelist_times(self, table_name: str, timestamp: int):
        # 設定 fraud detector 白名單更新時間
        message_hash = hashlib.sha256(f"{WhiteListStatusEnum.FRAUD_DETECTOR_WHITELIST.value}".encode('utf-8')).hexdigest()
        self.conn.hset(message_hash, table_name, timestamp)

    def get_fraud_update_whitelist_times(self):
        # 取得 fraud detector 白名單更新時間
        message_hash = hashlib.sha256(f"{WhiteListStatusEnum.FRAUD_DETECTOR_WHITELIST.value}".encode('utf-8')).hexdigest()
        white_list_table_name_list = [member.value for member in WhiteListTableNameEnum.__members__.values()]
        return self.conn.hmget(message_hash, white_list_table_name_list)

    def set_fraud_user_usage_frequency(self, user_id: str, target_service: str, category: str, last_update_time: int, send_count: int) -> int:
        # 設定使用者目前的訊息使用頻率，當 key 值存在時，表示僅需更新次數，不存在表示為此時間段全新的紀錄
        target_hash = hashlib.sha256(f"{target_service}-{user_id}-{category}".encode('utf-8')).hexdigest()
        now_count = self.conn.hincrby(target_hash, UserFrequencyColumn.SENT_EVENT_COUNT.value, send_count)

        # 如果這是新的 key (即計數從 0 增加到 send_count)，則設定逾期時間
        if now_count == send_count:
            self.conn.hset(target_hash, UserFrequencyColumn.LAST_UPDATE_TIME.value, last_update_time)

            timeouts = {
                UserFrequencyCategory.SECOND.value: 1,
                UserFrequencyCategory.MINUTE.value: 60
            }
            timeout = timeouts.get(category, 60)
            if timeout == 60 and category != UserFrequencyCategory.MINUTE.value:
                logger.warning(f"get unexpected category in {self.__name__}, set timeout as default value")

            self.conn.expire(target_hash, timeout)
        return now_count

    def get_fraud_user_usage_frequency(self, user_id: str, target_service: str, category: str):
        # 查詢使用者目前的訊息使用頻率
        target_hash = hashlib.sha256(f"{target_service}-{user_id}-{category}".encode('utf-8')).hexdigest()
        user_frequency_column_list = [member.value for member in UserFrequencyColumn.__members__.values()]
        return self.conn.hmget(target_hash, user_frequency_column_list)


redis_object = RedisImplement()
