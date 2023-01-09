# -*- coding: utf-8 -*-
# !/usr/bin/python3
# @Time    : 2022/12/28 15:00
# @Author  : VocabVictor
# @Email   : vocabvictor@gmail.com
# @File    : update.py
# @Software: PyCharm,VsCode
# @Description: 用于更新博客的工具类
# @Support Python Version: 3.5+
# 以下是一个为hugo博客进行持续集成部署一个工具类，他的功能如下
'''
    1. 启动本地hugo服务
    2. 监听本地文件变化，自动更新
    3. 自动提交到github和gitee
    4. 自动提交到腾讯云oss
    5. 不管是gitee,github还是腾讯云oss,都只会提交最近更新文件，不会重复提交
    6. 自动更新腾讯云cdn
    7. 自动更新腾讯云cdn的缓存
    8. 拥有一个简单的界面
    9. 该工具类可以在windows和linux上运行
'''
from tencentool import TencentTool
from os import chdir
from subprocess import Popen, PIPE
from os import system
class AutoCommit:
    def __init__(self):
        self.modified_files = []

    def set(self,dict):
        self.__dict__.update(dict)
        # 如果有博客文件路径，就设置博客文件路径
        if self.blog_path:
            chdir(self.blog_path)
        # 如果自动启动本地服务，就启动本地服务
        if self.hugo:
            info = self.start_server()
        else:
            info = None
        self.tencent_tool = TencentTool(
            secret_id = self.secret_id,
            secret_key = self.secret_key,
            region = self.oss_region,
            bucket = self.oss_bucket,
            cdn_domain = self.cdn_domain
        )
        return info

    def find_modified_files(self):
        # 这里应该写代码来检测文件变化
        pass

    def get_modified_files(self):
        # 这里应该写代码来检测文件变化
        pass

    def commit_to_github(self):
        # 这里应该写代码来提交到 github
        pass

    def commit_to_gitee(self):
        # 这里应该写代码来提交到 gitee
        pass

    def git_commit(self):
        # 这里应该写代码来提交到 github 和 gitee
        system('git add .')
        system('git commit -m "update"')
        system('git push origin main')

    def update_oss(self):
        # 这里应该写代码来更新腾讯云 oss
        pass

    def update_cdn(self):
        # 这里应该写代码来更新腾讯云 cdn
        pass

    def update_cdn_cache(self):
        # 这里应该写代码来更新腾讯云 cdn 的缓存
        pass

    def start_server(self):
        # 这里应该写代码来启动本地服务
        self.hugo_cmd = Popen(["hugo", "server"], stdout=PIPE, stderr=PIPE)
        return self.hugo_cmd

    def stop_server(self):
        # 这里应该写代码来停止本地服务
        self.hugo_cmd.kill()
        del self.hugo_cmd
        return None

    def deploy(self):
        # 这里应该写代码来部署到服务器
        pass

