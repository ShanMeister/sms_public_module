#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import http.client
import json
import os
import sys
import time
import requests
import uvicorn
from threading import Thread, Event, Timer
import pytest
import pandas as pd

from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv
from loguru import logger
from starlette.requests import Request

load_dotenv('tests/integration/sms_fraud_detector/.env')

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from app.enums.risk_message import RiskMessage
from tests.library.util import generate_random_string, get_target_key_in_dict, generate_signature_by_content
from app.enums.fraud_detector_postback_enum import FraudDetectorPostbackEnum
from app.enums.line_bot_event_type import LineBotEventType
from app.enums.risk_status import RiskStatus

app_test = FastAPI()

logger.remove()
logger.add("logs/test_{time:YYYY-MM-DD}.log", level=os.getenv('SCX_LOG_LEVEL', 'DEBUG'))

# 儲存後續伺服器回傳需進行 assert 的結果
normal_sms_assert_results = {}
# 儲存後續用於建立 postback event 的結果
postback_event_assert_results = {}
# 創建一個 threading.Event 來判斷是否要推進下一步
server_stop_event = Event()
# 創造用來控制發送 postback event 的 threading.Event
start_to_send_postback_event = Event()


def run_app(server_app):
    server_instance = uvicorn.Config(
        app=server_app,
        host=os.getenv('SCX_RUN_TEST_HOST'),
        port=int(os.getenv('SCX_RUN_TEST_PORT')),
        # 因 unicorn 在 thread 中執行，如果印出預設的 logging，會因為 thread safe 議題出錯，此處將 log level 調高，只在真正錯誤時印出
        log_level="warning"
    )
    server = uvicorn.Server(config=server_instance)

    # 宣告 api server 運行一段時間，接收由測試目標給予的 response，時間到則結束
    def stop_server():
        global server_stop_event
        server_stop_event.set()
        server.should_exit = True

    # 設置停止服務器的計時器
    run_interval = int(os.getenv('SCX_TEST_SERVER_RUN_TIME', 60))
    if not run_interval:
        raise Exception('server run time format error, please check the .env file')
    timer = Timer(run_interval, stop_server)
    timer.start()

    @app_test.post('/assert')
    async def assert_endpoint(request: Request):
        global normal_sms_assert_results, postback_event_assert_results, start_to_send_postback_event
        content = await request.json()
        flex_message = content['flex_message']
        reply_token = content['reply_token']
        logger.info(f"get response for reply token: {reply_token}, {flex_message}")

        if reply_token in normal_sms_assert_results.keys():
            flex_content = json.loads(flex_message)
            resp_text = get_target_key_in_dict(flex_content, 'contents.body.contents.contents', 'contents')
            # 當前可供辨識的 key 值僅有顏色欄位，因此此處抓指定色碼的顏色，當作判別是否為目標元件的依據
            target_content = None
            for element in resp_text:
                try:
                    if element['color'] == "#1C305F" or element['color'] == "#FFBB00":
                        target_content = element
                        break
                except:
                    # 為了避免可能有欄位沒有指定 color，如果觸發 exception 就什麼都不做
                    pass

            if target_content:
                resp_text = target_content['text']
                logger.debug(f"resp text: {resp_text}, target: {normal_sms_assert_results[reply_token]}")
                if resp_text == normal_sms_assert_results[reply_token]:
                    normal_sms_assert_results.update({reply_token: True})
        else:
            logger.debug(f"unknown reply token: {reply_token}")

        # 更新 postback 的準備狀況
        if reply_token in postback_event_assert_results.keys():
            postback_event_assert_results[reply_token]['status'] = True
            postback_status_list = [element['status'] for element in postback_event_assert_results.values()]
            if all(postback_status_list) and not start_to_send_postback_event.is_set():
                start_to_send_postback_event.set()
        return 'OK'

    server.run()


Thread(target=run_app, args=(app_test,)).start()


def load_sms_content():
    data = pd.read_csv("./storage/tests/SMS_all_domains_unique.csv")
    dict_data = data.to_dict('records')
    return dict_data


sms_data = load_sms_content()

protocol = os.getenv('SCX_WEBHOOK_PROTOCOL', 'https')
api_path = os.getenv('SCX_WEBHOOK_API_PATH', 'callback')
host = os.getenv('SCX_WEBHOOK_HOST')
port = os.getenv('SCX_WEBHOOK_PORT')
if not host or not protocol or not api_path:
    raise Exception(f"webhook info not set, protocol: {protocol}, host: {host}, port: {port}, api path: {api_path}")
webhook_url = f"{protocol}://{host}/{api_path}" if port is None else f"{protocol}://{host}:{port}/{api_path}"

channel_secret = os.getenv('LINE_CHANNEL_SECRET')
if not channel_secret:
    raise Exception('channel secret is not set')


def generate_webhook_event(event_type, content=None):
    if content is None:
        content = {}
    # 生成需要動態產生的 token
    webhook_event_id = "ID-" + generate_random_string(9)
    reply_token = hashlib.md5(webhook_event_id.encode('utf-8')).hexdigest()
    # 正常的 line bot 使用者 id 為 U + 32 字，測試改用 T 開頭作為區別
    user_id = content.get('user_id', "T" + generate_random_string(32))

    # line bot 後端各個事件的共通欄位
    base_event = {
        "replyToken": reply_token,
        "webhookEventId": webhook_event_id,
        "source": {
            "userId": user_id,
            "type": "user"
        },
        "timestamp": round(time.time() * 1000),
    }

    match event_type:
        case LineBotEventType.MESSAGE.value:
            global normal_sms_assert_results, postback_event_assert_results
            message = content['message']
            risk_key = content['result'].upper()
            normal_sms_assert_results.update({reply_token: RiskMessage[risk_key].value})

            postback_base_content = {
                reply_token: {
                    'event_id': webhook_event_id,
                    'user_id': user_id,
                    'status': False,
                }
            }
            # 紀錄後續 postback 用於建立 event 所需的資訊
            match risk_key.lower():
                case RiskStatus.NOT_SUSPICIOUS.value:
                    postback_base_content[reply_token]['postback_event'] = FraudDetectorPostbackEnum.NEGATIVE.value
                    postback_event_assert_results.update(postback_base_content)
                case RiskStatus.SUSPICIOUS.value:
                    postback_base_content[reply_token]['postback_event'] = FraudDetectorPostbackEnum.POSITIVE.value
                    postback_event_assert_results.update(postback_base_content)
                case _:
                    logger.debug(f"event has no postback situation: {risk_key}")

            base_event.update({
                "type": LineBotEventType.MESSAGE.value,
                "message": {
                    "type": "text",
                    "id": webhook_event_id,
                    "text": message
                },
                "mode": "active"
            })
        case LineBotEventType.FOLLOW.value:
            base_event.update({
                "type": LineBotEventType.FOLLOW.value
            })
        case LineBotEventType.JOIN.value:
            # 正常的 line bot 群組 id 為 C + 32 字，測試改用 G 開頭作為區別
            group_id = "G" + generate_random_string(32)
            base_event.update({
                "type": LineBotEventType.JOIN.value,
                "source": {
                    "type": "group",
                    "groupId": group_id
                }
            })
        case LineBotEventType.POSTBACK.value:
            data = content.get("data", "")
            user_id = content.get('user_id', '')
            base_event.update({
                "type": LineBotEventType.POSTBACK.value,
                "postback": {
                    "data": data
                }
            })
        case _:
            logger.debug(f"unknown event type: {event_type}")
    return {'events': [base_event]}


def send_event_to_webhook(event_type, content=None):
    if content is None:
        content = {}
    event_content = generate_webhook_event(event_type, content)
    updated_request_body_str = json.dumps(event_content)

    # Generate request signature
    signature = generate_signature_by_content(channel_secret, updated_request_body_str)

    headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': signature
    }

    response = requests.post(webhook_url, data=updated_request_body_str, headers=headers)
    elapsed_time = response.elapsed.total_seconds()

    assert response.status_code == http.client.OK, f"response status code: {response.status_code} for event: {updated_request_body_str}"
    assert elapsed_time <= 1, f"response costs {elapsed_time} seconds for event: {updated_request_body_str}"


@pytest.mark.run(order=1)
def test_welcome_event_api_endpoint():
    # 發送新使用者 event
    send_event_to_webhook(LineBotEventType.FOLLOW.value)

    # 發送新群組 event
    send_event_to_webhook(LineBotEventType.JOIN.value)


@pytest.mark.run(order=2)
@pytest.mark.parametrize("test_sms_content", sms_data)
def test_normal_sms_api_endpoint(test_sms_content):
    # 發送要拋出進行測試的 event 內容
    send_event_to_webhook(LineBotEventType.MESSAGE.value, test_sms_content)


@pytest.fixture(scope="function")
def wait_until_server_is_ready():
    global start_to_send_postback_event
    if not start_to_send_postback_event.is_set():
        start_to_send_postback_event.wait()


@pytest.mark.run(order=3)
@pytest.mark.usefixtures("wait_until_server_is_ready")
def test_postback_event_api_endpoint():
    global postback_event_assert_results
    for element in postback_event_assert_results.items():
        reply_token, content = element
        # 依據 order 2 建立的 event，觸發 postback event
        event_id = content['event_id']
        postback_event = content['postback_event']
        user_id = content['user_id']
        postback_content = {
            'user_id': user_id,
            'data': f"report={postback_event}&event={event_id}"
        }

        send_event_to_webhook(LineBotEventType.POSTBACK.value, postback_content)


@pytest.fixture(scope="function")
def wait_until_server_is_stopped():
    global server_stop_event
    if not server_stop_event.is_set():
        server_stop_event.wait()


@pytest.mark.run(order=4)
@pytest.mark.usefixtures("wait_until_server_is_stopped")
def test_assert_results():
    global normal_sms_assert_results
    for element in normal_sms_assert_results.items():
        reply_token, status = element
        assert status is True, f"reply key {reply_token} assert failed: {status}"
