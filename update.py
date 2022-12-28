# -*- coding: utf-8 -*-
# !/usr/bin/python3
# @Time    : 2020/12/28 15:00
# @Author  : VocabVictor
# @Email   : vocabvictor#gmail.com
# @File    : update.py
# @Software: PyCharm,VsCode
# @Description: 用于更新博客的工具类

# 以下是一个为hugo博客进行持续集成部署一个工具类，他的功能如下
'''
    1. 启动本地hugo服务
    2. 监听本地文件变化，自动更新
    3. 自动提交到github和gitee
    4. 自动提交到腾讯云oss
    5. 不管是gitee,github还是腾讯云oss,都只会提交最近更新文件，不会重复提交
    6. 自动更新腾讯云cdn
    7. 自动更新腾讯云cdn的缓存
    8. 拥有一个简单的GUI界面，可以可视化上面的操作,该界面使用python的tkinter模块实现，拥有一个布局合理的界面
        8.1 该界面可以选择是否启动本地hugo服务
        8.2 该界面可以选择是否自动提交到github和gitee
        8.3 该界面可以选择是否自动提交到腾讯云oss
        8.4 该界面可以选择是否自动更新腾讯云cdn
        8.5 该界面可以选择是否自动更新腾讯云cdn的缓存
        8.6 该界面会显示当前的操作状态
        8.7 该界面会显示当前的操作日志
        8.9 该界面会显示更新和提交的文件列表
    9. 该工具类可以在windows和linux上运行
'''

import os
import subprocess
import github
import qcloud_cos
import qcloud_cdn
import tkinter

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

# 以下类用于实现上文中所说的简单的GUI界面
class GUI:
    def __init__(self, update):
        # 初始化
        # update是一个Update对象
        self.update = update
        # 创建窗口
        self.root = tkinter.Tk()
        # 设置窗口标题
        self.root.title('VocabVictor的博客更新工具')
        # 设置窗口大小
        self.root.geometry('800x600')
        # 设置窗口不可变
        self.root.resizable(0, 0)
        # 设置窗口关闭时的操作
        self.root.protocol('WM_DELETE_WINDOW', self.close_window)
        # 设置窗口图标
        self.root.iconbitmap('favicon.ico')
        # 创建组件
        self.create_widgets()

    def create_widgets(self):
        # 创建组件
        self.create_menu()
        self.create_status()
        self.create_log()
        self.create_update_files()
        self.create_buttons()

    def create_menu(self):
        # 创建菜单
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu_file = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='文件', menu=self.menu_file)
        self.menu_file.add_command(label='退出', command=self.close_window)

    def create_status(self):
        # 创建状态
        self.status = tkinter.Label(self.root, text='当前状态：' + self.update.status)
        self.status.pack()

    def create_log(self):
        # 创建日志
        self.log = tkinter.Label(self.root, text='操作日志：' + '\r '.join(self.update.log))
        self.log.pack()
    
    def create_update_files(self):
        # 创建更新文件
        self.update_files = tkinter.Label(self.root, text='更新文件：' + '\r '.join(self.update.update_files))
        self.update_files.pack()
    
    def create_buttons(self):
        # 创建按钮
        self.buttons = tkinter.Frame(self.root)
        self.buttons.pack()
        self.local_hugo_service = tkinter.Button(self.buttons, text='启动本地hugo服务', command=self.update.start_local_hugo_service)
        self.local_hugo_service.pack(side='left')
        self.auto_commit_github = tkinter.Button(self.buttons, text='自动提交到github', command=self.update.auto_commit_github)
        self.auto_commit_github.pack(side='left')
        self.auto_commit_gitee = tkinter.Button(self.buttons, text='自动提交到gitee', command=self.update.auto_commit_gitee)
        self.auto_commit_gitee.pack(side='left')
        self.auto_commit_qcloud_oss = tkinter.Button(self.buttons, text='自动提交到腾讯云oss', command=self.update.auto_commit_qcloud_oss)
        self.auto_commit_qcloud_oss.pack(side='left')
        self.auto_update_qcloud_cdn = tkinter.Button(self.buttons, text='自动更新腾讯云cdn', command=self.update.auto_update_qcloud_cdn)
        self.auto_update_qcloud_cdn.pack(side='left')
        self.auto_update_qcloud_cdn_cache = tkinter.Button(self.buttons, text='自动更新腾讯云cdn的缓存', command=self.update.auto_update_qcloud_cdn_cache)
        self.auto_update_qcloud_cdn_cache.pack(side='left')

    def close_window(self):
        # 关闭窗口
        self.root.destroy()
    
    def update_status(self):
        # 更新状态
        self.status.config(text='当前状态：' + self.update.status)
    
    def update_log(self):
        # 更新日志
        self.log.config(text='操作日志：' + '\r '.join(self.update.log))
    
    def update_update_files(self):
        # 更新更新文件
        self.update_files.config(text='更新文件：' + '\r '.join(self.update.update_files))
    
    def update_buttons(self):
        # 更新按钮
        if self.update.local_hugo_service:
            self.local_hugo_service.config(state='disabled')
        else:
            self.local_hugo_service.config(state='normal')
        if self.update.auto_commit_github:
            self.auto_commit_github.config(state='disabled')
        else:
            self.auto_commit_github.config(state='normal')
        if self.update.auto_commit_gitee:
            self.auto_commit_gitee.config(state='disabled')
        else:
            self.auto_commit_gitee.config(state='normal')
        if self.update.auto_commit_qcloud_oss:
            self.auto_commit_qcloud_oss.config(state='disabled')
        else:
            self.auto_commit_qcloud_oss.config(state='normal')
        if self.update.auto_update_qcloud_cdn:
            self.auto_update_qcloud_cdn.config(state='disabled')
        else:
            self.auto_update_qcloud_cdn.config(state='normal')
        if self.update.auto_update_qcloud_cdn_cache:
            self.auto_update_qcloud_cdn_cache.config(state='disabled')
        else:
            self.auto_update_qcloud_cdn_cache.config(state='normal')

    def update_all(self):
        # 更新所有
        self.update_status()
        self.update_log()
        self.update_update_files()
        self.update_buttons()
        self.root.after(1000, self.update_all)

class Update:
    def __init__(self):
        # 初始化参数
        self.local_hugo_service = False  # 是否启动本地hugo服务
        self.auto_commit_github = False  # 是否自动提交到github
        self.auto_commit_gitee = False  # 是否自动提交到gitee
        self.auto_commit_qcloud_oss = False  # 是否自动提交到腾讯云oss
        self.auto_update_qcloud_cdn = False  # 是否自动更新腾讯云cdn
        self.auto_update_qcloud_cdn_cache = False  # 是否自动更新腾讯云cdn的缓存
        self.status = '初始化完成'  # 当前的操作状态
        self.log = []  # 操作日志
        self.update_files = []  # 更新和提交的文件列表

    def start_local_hugo_service(self):
        # 启动本地hugo服务
        self.local_hugo_service = True
        self.status = '启动本地hugo服务'
        subprocess.run(['hugo', 'server', '-D'])  # 运行hugo命令启动服

    def listen_local_file_change(self):
        # 监听本地文件变化，自动更新
        self.status = '监听本地文件变化'
        while True:
            # 执行文件监听操作
            updated_files = []  # 记录更新的文件列表
            # 遍历文件夹，检查文件是否有更新
            for root, dirs, files in os.walk('.'):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 检查文件是否有更新
                    if self.check_file_updated(file_path):
                        updated_files.append(file_path)
            # 如果有更新的文件，则进行相应的操作
            if updated_files:
                self.update_files.extend(updated_files)  # 记录更新的文件
                self.status = '检测到文件更新'
                self.log.append('检测到以下文件更新：\n' + '\n'.join(updated_files))
                if self.auto_commit_github:  # 如果自动提交到github，则执行提交操作
                    self.commit_to_github(updated_files)
                if self.auto_commit_gitee:  # 如果自动提交到gitee，则执行提交操作
                    self.commit_to_gitee(updated_files)
                if self.auto_commit_qcloud_oss:  # 如果自动提交到腾讯云oss，则执行提交操作
                    self.commit_to_qcloud_oss(updated_files)
                if self.auto_update_qcloud_cdn:  # 如果自动更新腾讯云cdn，则执行更新操作
                    self.update_qcloud_cdn(updated_files)
                if self.auto_update_qcloud_cdn_cache: # 如果自动更新腾讯云cdn的缓存，则执行更新操作
                    self.update_qcloud_cdn_cache(updated_files)
                self.status = '文件更新完成'
                self.log.append('文件更新完成：\n' + '\n'.join(updated_files))

    def commit_to_github(self, updated_files):
        # 自动提交到github
        self.status = '正在提交到github'
        # 使用github模块进行提交
        github.commit(updated_files)
        self.log.append('成功提交到github：\n' + '\n'.join(updated_files))

    def commit_to_gitee(self, updated_files):
        # 自动提交到gitee
        self.status = '正在提交到gitee'
        # 使用gitee模块进行提交
        gitee.commit(updated_files)
        self.log.append('成功提交到gitee：\n' + '\n'.join(updated_files))

    def commit_to_qcloud_oss(self, updated_files):
        # 自动提交到腾讯云oss
        self.status = '正在提交到腾讯云oss'
        # 使用qcloud_oss模块进行提交
        qcloud_oss.commit(updated_files)
        self.log.append('成功提交到腾讯云oss：\n' + '\n'.join(updated_files))

    def update_qcloud_cdn(self, updated_files):
        # 自动更新腾讯云cdn
        self.status = '正在更新腾讯云cdn'
        # 使用qcloud_cdn模块进行更新
        qcloud_cdn.update(updated_files)
        self.log.append('成功更新腾讯云cdn：\n' + '\n'.join(updated_files))

    def update_qcloud_cdn_cache(self, updated_files):
        # 自动更新腾讯云cdn的缓存
        self.status = '正在更新腾讯云cdn的缓存'
        # 使用qcloud_cdn模块进行更新
        qcloud_cdn.update_cache(updated_files)
        self.log.append('成功更新腾讯云cdn的缓存：\n' + '\n'.join(updated_files))
    
    def check_file_updated(self, file_path):
        # 检查文件是否有更新
        last_update_time = self.get_file_last_update_time(file_path)  # 获取文件上一次更新时间
        return last_update_time > self.get_last_commit_time(file_path)  # 如果文件上一次更新时间晚于上一次提交时间，则文件有更新

    def get_file_last_update_time(self, file_path):
        # 获取文件上一次更新时间
        return os.stat(file_path).st_mtime  # 返回文件最后修改时间

    def get_last_commit_time(self, file_path):
        # 获取文件上一次提交时间
        # 使用git命令获取文件上一次提交时间
        last_commit_time = subprocess.run(['git', 'log', '-1', '--format=%at', file_path], stdout=subprocess.PIPE).stdout
        return int(last_commit_time)  # 返回文件上一次提交时间

        
if __name__ == '__main__':
    # 如果是直接运行本文件，则执行以下代码
    # 创建一个更新工具类实例
    updater = Update()
    # 创建一个app实例
    app = GUI(updater)

