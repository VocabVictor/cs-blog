import asyncio
import aiohttp
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import os

async def upload_file(bucket, key, file_path, secret_id, secret_key):
    # 配置密钥信息和默认区域
    config = CosConfig(Region='ap-nanjing', SecretId=secret_id, SecretKey=secret_key)

    # 创建客户端
    client = CosS3Client(config)

    # 检查文件大小
    file_size = os.path.getsize(file_path)
    if file_size < 1024 * 1024:
        # 如果文件小于 1MB，直接上传
        response = client.put_object(
            Bucket=bucket,
            Key=key,
            Body=open(file_path, 'rb'),
        )
    else:
        # 否则，启动分片上传
        response = await upload_file_in_parts(bucket, key, file_path, client)
    print(response)
    return response

async def upload_file_in_parts(bucket, key, file_path, client):
    # 初始化分片上传任务
    response = client.create_multipart_upload(
        Bucket=bucket,
        Key=key,
    )
    upload_id = response['UploadId']

    # 读取文件的分片
    etags = []
    part_numbers = []
    with open(file_path, 'rb') as file:
        part_number = 1
        while True:
            chunk = file.read(1024 * 1024)  # 每次读取 1MB 的数据
            if not chunk:
                break

            # 使用协程并发上传分片
            async with aiohttp.ClientSession() as session:
                response = await client.upload_part(
                    Bucket=bucket,
                    Key=key,
                    Body=chunk,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    _session=session,
                )
                etag = response['ETag']
                etags.append(etag)
                part_numbers.append(part_number)
                part_number += 1

    # 完成分片上传任务
    parts = [{'ETag': etag, 'PartNumber': part_number} for etag, part_number in zip(etags, part_numbers)]
    response = client.complete_multipart_upload(
        Bucket=bucket,
        Key=key,
        UploadId=upload_id
    )

    return response

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(upload_file(
        bucket='cs-blog-1304916025',
        key='python/test.py',
        file_path=r'F:\cs-blog\test.py',
        secret_id='AKIDPiAgEoS8f6c9f5b7TfuGmEc0NizCIKLD',
        secret_key='0U3hIj5FNVcf2Tly8ayMpCQXUUZ9Nemt'
    ))
    loop.close()

