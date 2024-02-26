#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os

from datetime import timedelta

from google.cloud import storage


class BucketController:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.download_url_expired_at = int(os.getenv('DOWNLOAD_URL_EXPIRED_AT'))

    def read_string_in_bucket(self, file_name: str):
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.get_blob(file_name)
        if blob is None:
            return None
        # 實際確認實作，此處名稱為 download_as_string 但其實後面是呼叫 download_as_bytes 且沒有任何型態轉換，因此需要額外 decode
        return blob.download_as_string().decode('utf-8')

    def write_string_in_bucket(self, content: str, file_name: str):
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(content)

    def get_all_files_in_bucket_prefix(self, prefix: str):
        # 取得 bucket 物件
        bucket = self.client.get_bucket(self.bucket_name)

        # 列出指定 bucket 和 prefix 內的所有物件
        return bucket.list_blobs(prefix=prefix)

    def generate_download_url(self, file_name: str):
        # 獲取指定的 Bucket
        bucket = self.client.get_bucket(self.bucket_name)

        # 獲取指定的 Blob
        blob = bucket.get_blob(file_name)

        # 設定網址有效時間，因 generate_signed_url 只接受 integer timestamp, datetime, or timedelta ，所以不用 arrow
        expiration_time = timedelta(seconds=self.download_url_expired_at)

        # 為 Blob 生成下載連結，設定網址有效期
        return blob.generate_signed_url(expiration=expiration_time)

    def write_bytes_to_bucket(self, content: io.BytesIO, file_name: str):
        # 獲取指定的 Bucket
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(file_name)
        content.seek(0)  # 確保content指標在開頭
        blob.upload_from_file(content)  # 將 content 傳入，而不是使用 upload_from_string

    def read_bytes_in_bucket(self, file_name: str):
        # 獲取指定的 Bucket
        bucket = self.client.get_bucket(self.bucket_name)

        # 讀取指定檔案的內容
        blob = bucket.blob(file_name)
        content = io.BytesIO()
        blob.download_to_file(content)
        content.seek(0)

        return content
