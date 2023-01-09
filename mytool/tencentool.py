# -*- coding: utf-8 -*-
# !/usr/bin/python3
# @Time    : 20223/1/9 15:00
# @Author  : VocabVictor
# @Email   : VocabVictor@gmail.com
# @File    : tencentool.py
# @Software: PyCharm,VsCode
# @Description: 腾讯云API调用类
# @Support Python Version: 3.5+

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from os.path import getsize
from aiohttp import ClientSession
from json import dumps
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.cdn.v20180606 import cdn_client, models
from os.path import relpath
from concurrent.futures import ThreadPoolExecutor, as_completed
class TencentTool:
    def __init__(self, blog_path,region, bucket, secret_id, secret_key,cdn_domain=None):

        # 配置cdn
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(secret_id, secret_key)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cdn.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        self.client = cdn_client.CdnClient(cred, "", clientProfile)

        # 配置cos
        # 配置密钥信息和默认区域
        self.config = CosConfig(
            Region=region, SecretId=secret_id, SecretKey=secret_key)
        # 创建cos客户端
        self.client = CosS3Client(self.config)

        # 保存参数
        self.blog_path = blog_path
        self.region = region
        self.bucket = bucket
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.cdn_domain = cdn_domain
        self.max_file_size = 1024 * 1024 * 500

    def upload_files(self, file_list):
        with ThreadPoolExecutor() as executor:
            # 提交所有任务
            futures = []
            for file_path in file_list:
                key = relpath(file_path, self.blog_path).replace('\\', '/')
                future = executor.submit(self.upload_file, key, file_path)
                futures.append(future)
            # 等待所有任务完成
            for future in as_completed(futures):
                print(future.result())

    def delete_files(self,file_list):
        with ThreadPoolExecutor() as executor:
            # 提交所有任务
            futures = []
            for file_path in file_list:
                key = relpath(file_path, self.blog_path).replace('\\', '/')
                future = executor.submit(self.del_file, key)
                futures.append(future)
            # 等待所有任务完成
            for future in as_completed(futures):
                print(future.result())        

    def del_file(self,key):
        self.client.delete_object(
            Bucket=self.bucket,
            Key=key
        )
        return key

    def upload_file(self,key,file_path):
        # 检查文件大小
        file_size = getsize(file_path)
        if file_size < self.max_file_size:
            # 如果文件小于 500MB，直接上传
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=open(file_path, 'rb'),
            )
        else:
            # 否则，启动分片上传
            self.upload_file_in_parts(key, file_path)
        return key

    def upload_file_in_parts(self, key, file_path):
        # 初始化分片上传任务
        response = self.client.create_multipart_upload(
            Bucket=self.bucket,
            Key=key,
        )
        upload_id = response['UploadId']

        # 读取文件的分片
        etags = []
        part_numbers = []
        with open(file_path, 'rb') as file:
            part_number = 1
            # 每次读取 1MB 的数据
            while True:
                chunk = file.read(1024 * 1024)  # 每次读取 1MB 的数据
                if not chunk:
                    break
                # 上传分片
                with ClientSession:
                    response = self.client.upload_part(
                        Bucket=self.bucket,
                        Key=key,
                        Body=chunk,
                        PartNumber=part_number,
                        UploadId=upload_id
                    )
                    etag = response['ETag']
                    etags.append(etag)
                    part_numbers.append(part_number)
                    part_number += 1

        # 完成分片上传任务
        parts = [{'ETag': etag, 'PartNumber': part_number}
                 for etag, part_number in zip(etags, part_numbers)]
        response = self.client.complete_multipart_upload(
            Bucket=self.bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts},
        )
        return response

    def refresh_cdn_cache(self, urls=None):
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.PurgeUrlsCacheRequest()
        if isinstance(urls, str):
            urls = [urls]
        elif not urls and self.cdn_domain:
            urls = [self.cdn_domain]
        params = {
            "Urls": urls
        }
        req.from_json_string(dumps(params))

        # 返回的resp是一个PurgeUrlsCacheResponse的实例，与请求对象对应
        resp = self.client.PurgeUrlsCache(req)
        # 输出json格式的字符串回包
        print(resp.to_json_string())