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
from os import system,walk
from os.path import getmtime,exists
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
            blog_path = self.blog_path,
            secret_id = self.secret_id,
            secret_key = self.secret_key,
            region = self.oss_region,
            bucket = self.oss_bucket,
            cdn_domain = self.cdn_domain
        )
        return info

    # 使用walk函数遍历文件，并且记录下文件的更新时间，并把这个文件保存起来
    # 当下一次启动时，如果检测到某一个文件不存在于字典，或者最后修改时间发生了变化，就把这个文件加入到modified_files列表中
    # 这样就可以检测到文件的变化了
    def get_modified_files(self):
        modified_files = []
        for root, dirs, files in walk(self.blog_path):
            for file in files:
                file_path = root + '/' + file
                if file_path in self.file_dict:
                    if self.file_dict[file_path] != getmtime(file_path):
                        modified_files.append(file_path)
                else:
                    self.file_dict[file_path] = getmtime(file_path)
                    modified_files.append(file_path)
        return modified_files, self.file_dict

    def del_files(self):
        del_modified_files = []
        for path in self.file_dict:
            if not exists(path):
                del_modified_files.append(path)
        self.file_dict = {key: value for key, value in self.file_dict.items() if key not in del_modified_files}
        return del_modified_files, self.file_dict
        
    def git_commit(self):
        # 这里应该写代码来提交到 github 和 gitee
        system('git add .')
        system('git commit -m "update"')
        system('git push origin main')

    def gitee_commit(self):
        system('git add .')
        system('git commit -m "update"')
        system('git push gitee main')

    def update_oss(self):
        # 这里应该写代码来更新腾讯云 oss
        modified_files, self.file_dict = self.get_modified_files()
        self.tencent_tool.upload_files(modified_files)  
        modified_files, self.file_dict = self.del_files()
        self.tencent_tool.delete_files(modified_files)
        return self.file_dict

    def update_cdn_cache(self):
        # 这里应该写代码来更新腾讯云 cdn
        self.tencent_tool.refresh_cdn_cache()

    def deploy(self):
        # 这里应该写代码来部署到服务器
        system('hugo')
        if self.github:
            self.git_commit()
        if self.gitee:
            self.gitee_commit()
        if self.tencentcloud_oss:
            self.update_oss()
        if self.tencentcloud_cdn:
            self.update_cdn()


    def start_server(self):
        # 这里应该写代码来启动本地服务
        self.hugo_cmd = Popen(["hugo", "server"], stdout=PIPE, stderr=PIPE)
        return self.hugo_cmd

    def stop_server(self):
        # 这里应该写代码来停止本地服务
        self.hugo_cmd.kill()
        return None

