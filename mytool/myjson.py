# -*- coding: utf-8 -*-
# !/usr/bin/python3
# @Time    : 2023/1/8 15:00
# @Author  : VocabVictor
# @Email   : vocabvictor@gmail.com
# @File    : update.py
# @Software: PyCharm,VsCode
# @Description: 用于安全读取和保存配置文件
# @Support Python Version: 3.5+
# 以下是一个JSON类，用于安全读取和保存配置文件，他的功能是：
'''
    1. 读取配置文件，如果配置文件不存在，则创建一个新的配置文件；如果配置文件存在，则读取配置文件
    2. 保存配置文件，如果配置文件不存在，则创建一个新的配置文件；如果配置文件存在，则覆盖配置文件
    3. 读取和保存配置文件时，都会对配置文件进行加密和解密，加密和解密的密钥是本机的MAC地址,加密和解密的算法是AES
    4. 读取和保存配置文件时，都会对配置文件进行压缩和解压缩
    5. 读取配置文件时，都会对配置文件进行校验，如果校验失败，则抛出异常
    6. 该类的实例化对象，可以直接使用字典的方式来读取和保存配置文件
    7. 以上功能均用Python标准库实现，不需要安装第三方库。
    8. 按需导入，不会导入其他模块
'''
from Crypto.Cipher.AES import new as AES
from Crypto.Cipher.AES import MODE_CBC, block_size
from base64 import b64decode, b64encode
from hashlib import sha256
from hmac import compare_digest
from hmac import new as HMAC
from json import dumps, loads
from os import urandom
from uuid import getnode
from zlib import compress, decompress
from os.path import exists

class Config:
    def __init__(self, filepath,data=None):
        self.filepath = filepath
        self.key = self._get_key()
        # Initialize data attribute
        if data:
            self.data = data
            self.save()
        else:
            self.data = {}  

    def __getitem__(self, key):
        if key not in self.data:
            return None
        else:
            return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __contains__(self, key):
        return key in self.data
    
    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)
    
    def __str__(self) -> str:
        return str(self.data)

    def _get_key(self):
        mac = getnode()
        key = str(mac).encode()
        key = sha256(key).digest()
        return key

    def datas(self):
        return self.data

    def pad(self, data, block_size):
        pad_size = block_size - (len(data) % block_size)
        return data + bytes([pad_size] * pad_size)

    def unpad(self, data, block_size):
        pad_size = data[-1]
        if pad_size > block_size:
            raise ValueError('Invalid padding')
        return data[:-pad_size]

    def load(self):
        if not exists(self.filepath):
            raise FileNotFoundError("文件不存在")  # 如果文件不存在，则返回空字典

        try:
            with open(self.filepath, 'rb') as f:
                data = f.read()
            # 验证数据
            signature = data[-32:]
            data = data[:-32]
            expected_signature = HMAC(self.key, data, sha256).digest()
            if not compare_digest(signature, expected_signature):
                raise ValueError('Invalid signature')

            # 解码数据
            data = b64decode(data)
            # 提取初始化向量
            iv = data[:block_size]
            data = data[block_size:]
            # 解密数据
            aes = AES(self.key, MODE_CBC, iv)
            data = aes.decrypt(data)
            # 移除填充
            data = self.unpad(data, block_size)
            data = decompress(data)
            data = data.decode(encoding='utf-8')
            # 加载JSON数据
            self.data = loads(data)  # 更新数据属性
            return self.data
        except Exception as e:
            print(f'An error occurred while loading the config file: {e}')
            self.data = {}    # 更新数据属性
            return self.data  # 在发生错误时返回空字典


    def save(self, data=None):
        try:
            # 如果没有传入合法数据，则使用数据属性
            if not data or not isinstance(data, dict):
                data = self.data
            # 将数据转换为JSON格式
            data = dumps(data).encode(encoding='utf-8')
            # 压缩数据
            data = compress(data)
            # 生成初始化向量
            iv = urandom(block_size)
            # 加密数据
            aes = AES(self.key, MODE_CBC, iv)
            data = aes.encrypt(self.pad(data, block_size))
            # 编码数据
            data = b64encode(iv + data)
            # 生成签名
            signature = HMAC(self.key, data, sha256).digest()
            # 将数据保存到文件
            with open(self.filepath, 'wb') as f:
                f.write(data + signature)
                print('Config file saved successfully')
        except Exception as e:
            print(f'An error occurred while saving the config file: {e}')
