# -*- coding: utf-8 -*-
# !/usr/bin/python3
# @Time    : 2023/1/9 15:00
# @Author  : VocabVictor
# @Email   : VocabVictor@gmail.com
# @File    : gui.py
# @Software: PyCharm,VsCode
# @Description: 用于可视化操作的GUI界面
# @Support Python Version: 3.5+
'''
拥有一个简单的GUI界面，可以可视化上面的操作,该界面使用python的tkinter模块实现，拥有一个布局合理的界面
    1 该界面可以选择是否启动本地hugo服务
    2 该界面可以选择是否自动提交到github和gitee
    3 该界面可以选择是否自动提交到腾讯云oss
    4 该界面可以选择是否自动更新腾讯云cdn的缓存
    5 该界面会显示当前的操作状态
    6 该界面会显示当前的操作日志
    7 该界面会显示更新和提交的文件列表
    8 该界面会显示当前的操作时间
    9 该界面能自动保存上次的操作状态，并且能自动加载和保存
    10 对于以上的所有操作，该界面都能自动保存上次的操作状态，并且能自动加载和保存
    11 对于保存的所有配置数据，该界面都能自动加密和解密，加密的秘钥与本机的mac地址有关，保证了数据的安全性
'''

import tkinter as tk
from myjson import Config
from update import AutoCommit

from time import sleep
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # 更改窗口的标题
        self.title('Hugo博客自动更新工具')

        # 核心工具类
        self.auto_commit = AutoCommit()
        self.config = None
        self.tkvar = {}

        self.load_config()
        self.init_tkvar()
        self.hugo_info = self.auto_commit.set(self.config.datas())

        # 在界面中放置各种控件，如 Checkbutton、Label、Button 等
        # variable 参数用于绑定变量，command 参数用于绑定事件

        # 首先设置一个frame,用于放置五个复选框
        self.frame = tk.Frame(self)
        # 设置五个个复选框，用于选择各种服务
        self.checkbutton_hugo = tk.Checkbutton(
            self.frame, text='自动启动本地 hugo 服务',variable=self.tkvar['hugo'])
        self.checkbutton_github = tk.Checkbutton(
            self.frame, text='自动提交到 github',variable=self.tkvar['github'])
        self.checkbutton_gitee = tk.Checkbutton(
            self.frame, text='自动提交到 gitee',variable=self.tkvar['gitee'])
        self.checkbutton_oss = tk.Checkbutton(
            self.frame, text='自动提交到腾讯云 oss',variable=self.tkvar['tencentcloud_oss'])
        self.checkbutton_cdn_cache = tk.Checkbutton(
            self.frame, text='自动更新腾讯云 cdn 的缓存',variable=self.tkvar['tencentcloud_cdn'])

        # 以下是四个列表组件，用于显示日志、文件列表、状态、时间
        # 由于列表组件比较特殊，所以需要使用 Listbox
        # 以下四个列表组件的数据都是从 auto_commit 中获取的
        # 由于 auto_commit 是一个线程，所以需要使用 queue 来传递数据
        self.textbox_frame = tk.Frame(self, bg='red')
        self.textbox_log = tk.Text(self.textbox_frame, width=50,height=10,bg='black', fg='green')
        self.textbox_files = tk.Text(self.textbox_frame, width=50,height=10,bg='black', fg='green')
        self.textbox_status = tk.Text(self.textbox_frame,bg='black', fg='green')
        self.textbox_time = tk.Listbox(self.textbox_frame, bg='black', fg='green')

        # 以下是三个按钮，用于全选，全不选，反选，上传到腾讯云oss,启动、停止、保存配置,提交到github和一键部署
        self.button_frame = tk.Frame(self)
        self.button_select_all = tk.Button(
            self.button_frame, text='全选', command=self.select_all)
        self.button_select_none = tk.Button(
            self.button_frame, text='全不选', command=self.select_none)
        self.button_select_invert = tk.Button(
            self.button_frame, text='反选', command=self.select_invert)
        self.button_upload = tk.Button(
            self.button_frame, text='上传到腾讯云oss', command=self.update_oss)
        self.button_cdn_cache = tk.Button(
            self.button_frame, text='更新腾讯云cdn的缓存', command=self.update_cdn_cache)
        self.button_start = tk.Button(
            self.button_frame, text='启动', command=self.start_server)
        self.button_stop = tk.Button(
            self.button_frame, text='停止', command=self.stop_server)
        self.button_save = tk.Button(
            self.button_frame, text='保存配置', command=self.save_config)
        self.button_github = tk.Button(
            self.button_frame, text='提交到github和gitee', command=self.git_commit)
        self.button_deploy = tk.Button(
            self.button_frame, text='一键部署', command=self.deploy)

        # 以下是各种输入框，用于输入各种配置
        self.entry_frame = tk.Frame(self)
        self.entry_blog_path = tk.Entry(
            self.entry_frame, textvariable=self.tkvar['blog_path'])
        self.entry_secret_id = tk.Entry(
            self.entry_frame, textvariable=self.tkvar['secret_id'])
        self.entry_secret_key = tk.Entry(
            self.entry_frame, textvariable=self.tkvar['secret_key'])
        self.entry_github_username = tk.Entry(
            self.entry_frame, textvariable=self.tkvar['github_username'])
        self.entry_github_password = tk.Entry(
            self.entry_frame, textvariable=self.tkvar['github_password'])
        self.entry_gitee_username = tk.Entry(
            self.entry_frame, textvariable=self.tkvar['gitee_username'])
        self.entry_gitee_password = tk.Entry(
            self.entry_frame, textvariable=self.tkvar['gitee_password'])
        self.entry_bucket = tk.Entry(
            self.entry_frame, textvariable=self.tkvar['oss_bucket'])
        self.entry_region = tk.Entry(
            self.entry_frame, textvariable=self.tkvar['oss_region'])
        self.entry_domain = tk.Entry(
            self.entry_frame, textvariable=self.tkvar['cdn_domain'])

        # 以下是各种标签，用于显示各种配置
        self.label_blog_path = tk.Label(self.entry_frame, text='博客路径')
        self.label_secret_id = tk.Label(self.entry_frame, text='secret_id')
        self.label_secret_key = tk.Label(self.entry_frame, text='secret_key')
        self.label_github_username = tk.Label(self.entry_frame, text='github 用户名')
        self.label_github_password = tk.Label(self.entry_frame, text='github 密码')
        self.label_gitee_username = tk.Label(self.entry_frame, text='gitee 用户名')
        self.label_gitee_password = tk.Label(self.entry_frame, text='gitee 密码')
        self.label_bucket = tk.Label(self.entry_frame, text='oss bucket')
        self.label_region = tk.Label(self.entry_frame, text='oss region')
        self.label_domain = tk.Label(self.entry_frame, text='cdn domain')

        self.grid()

        if self.hugo_info:
            self.log('本地hugo服务已经启动')
        self.log('初始化完成')

    def log(self, msg):
        msg = msg + '\n'
        self.textbox_log.insert("end",msg,("stdout",))

    def grid(self):
        # 使用 grid 布局
        # sticky 参数用于控制控件的对齐方式
        # columnspan 参数用于控制控件所占的列数
        # row 参数用于控制控件所在的行
        # column 参数用于控制控件所在的列
        # 复选框按钮在左上角纵向排列，每个按钮占用 2 列
        self.frame.grid(row=0, column=0, sticky='w', columnspan=2)
        self.checkbutton_hugo.grid(row=0, column=0, sticky='w', columnspan=2)
        self.checkbutton_github.grid(row=1, column=0, sticky='w', columnspan=2)
        self.checkbutton_gitee.grid(row=2, column=0, sticky='w', columnspan=2)
        self.checkbutton_oss.grid(row=3, column=0, sticky='w', columnspan=2)
        self.checkbutton_cdn_cache.grid(row=4, column=0, sticky='w', columnspan=2)


        # 列举控件在中间纵向排列，每个控件占用 4 列
        self.textbox_frame.grid(row=1, column=0, sticky='w', columnspan=4)
        self.textbox_files.grid(row=0, column=0, sticky='w', columnspan=2)
        self.textbox_log.grid(row=0, column=2, sticky='w', columnspan=2)
        # self.textbox_status.grid(row=5, column=0)
        # self.textbox_time.grid(row=8, column=0)

        # 文本框在右上角纵向排列，每个文本框占用 2 列,一行两个，一共四行
        self.entry_frame.grid(row=0, column=2, sticky='e', columnspan=8)
        self.label_blog_path.grid(row=0, column=0, sticky='w', columnspan=2)
        self.entry_blog_path.grid(row=0, column=2, sticky='e', columnspan=2)
        self.label_secret_id.grid(row=0, column=4, sticky='w', columnspan=2)
        self.entry_secret_id.grid(row=0, column=6, sticky='e', columnspan=2)
        self.label_secret_key.grid(row=1, column=0, sticky='w', columnspan=2)
        self.entry_secret_key.grid(row=1, column=2, sticky='e', columnspan=2)
        self.label_github_username.grid(row=1, column=4, sticky='w', columnspan=2)
        self.entry_github_username.grid(row=1, column=6, sticky='e', columnspan=2)
        self.label_github_password.grid(row=2, column=0, sticky='w', columnspan=2)
        self.entry_github_password.grid(row=2, column=2, sticky='e', columnspan=2)
        self.label_gitee_username.grid(row=2, column=4, sticky='w', columnspan=2)
        self.entry_gitee_username.grid(row=2, column=6, sticky='e', columnspan=2)
        self.label_gitee_password.grid(row=3, column=0, sticky='w', columnspan=2)
        self.entry_gitee_password.grid(row=3, column=2, sticky='e', columnspan=2)
        self.label_bucket.grid(row=3, column=4, sticky='w', columnspan=2)
        self.entry_bucket.grid(row=3, column=6, sticky='e', columnspan=2)
        self.label_region.grid(row=4, column=0, sticky='w', columnspan=2)
        self.entry_region.grid(row=4, column=2, sticky='e', columnspan=2)
        self.label_domain.grid(row=4, column=4, sticky='w', columnspan=2)
        self.entry_domain.grid(row=4, column=6, sticky='e', columnspan=2)

        # 按钮在右下角纵向排列，每个按钮占用 2 列
        self.button_frame.grid(row=2, column=0, sticky='e', columnspan=14)
        self.button_select_all.grid(row=0, column=0, sticky='e', columnspan=2)
        self.button_select_none.grid(row=0, column=2, sticky='e', columnspan=2)
        self.button_select_invert.grid(row=0, column=4, sticky='e', columnspan=2)
        self.button_upload.grid(row=0, column=6, sticky='e', columnspan=2)
        self.button_start.grid(row=0, column=8, sticky='e', columnspan=2)
        self.button_stop.grid(row=0, column=10, sticky='e', columnspan=2)
        self.button_save.grid(row=0, column=12, sticky='e', columnspan=2)
        self.button_github.grid(row=0, column=14, sticky='e', columnspan=2)
        self.button_deploy.grid(row=0, column=16, sticky='e', columnspan=2)

    def start_server(self):
        # 启动服务
        if self.hugo_info:
            self.log('服务已经启动')
        else:
            self.hugo_info = self.auto_commit.start_server()
            self.log('服务启动完成')
    
    def git_commit(self):
        # git 提交
        self.auto_commit.git_commit()
        self.log('git commit 完成')

    def stop_server(self):
        # 停止服务
        if self.hugo_info:
            self.hugo_info = self.auto_commit.stop_server()
            self.log('服务停止完成')
        else:
            self.log('服务未启动')

    def update_oss(self):
        # 更新 OSS
        self.config['file_dict'] = self.auto_commit.update_oss()
        self.save_config()
        self.log('更新 OSS 完成')

    def update_cdn_cache(self):
        # 更新 CDN 缓存
        self.auto_commit.update_cdn_cache()
        self.log('更新 CDN 缓存完成')

    def deploy(self):
        # 部署
        self.auto_commit.deploy()
        self.log('部署完成')

    def select_all(self):
        # 全选
        self.tkvar['hugo'].set(True)
        self.tkvar['github'].set(True)
        self.tkvar['gitee'].set(True)
        self.tkvar['tencentcloud_oss'].set(True)
        self.tkvar['tencentcloud_cdn'].set(True)

    def select_none(self):
        # 全不选
        self.tkvar['hugo'].set(False)
        self.tkvar['github'].set(False)
        self.tkvar['gitee'].set(False)
        self.tkvar['tencentcloud_oss'].set(False)
        self.tkvar['tencentcloud_cdn'].set(False)
    
    def select_invert(self):
        # 反选
        self.tkvar['hugo'].set(not self.tkvar['hugo'].get())
        self.tkvar['github'].set(not self.tkvar['github'].get())
        self.tkvar['gitee'].set(not self.tkvar['gitee'].get())
        self.tkvar['tencentcloud_oss'].set(not self.tkvar['tencentcloud_oss'].get())
        self.tkvar['tencentcloud_cdn'].set(not self.tkvar['tencentcloud_cdn'].get())

    def save_config(self):
        # 保存配置到 self.config 中
        for key in self.tkvar:
            self.config[key] = self.tkvar[key].get()
        # 保存配置到 config.json 文件中
        self.config.save()

    def init_tkvar(self):
        # 初始化tkvar
        # 以下是CheckBox的默认值
        self.tkvar['hugo'] = tk.BooleanVar(value=self.config['hugo'])
        self.tkvar['github'] = tk.BooleanVar(value=self.config['github'])
        self.tkvar['gitee'] = tk.BooleanVar(value=self.config['gitee'])
        self.tkvar['tencentcloud_oss'] = tk.BooleanVar(
            value=self.config['tencentcloud_oss'])
        self.tkvar['tencentcloud_cdn'] = tk.BooleanVar(
            value=self.config['tencentcloud_cdn'])

        # 以下是Entry的默认值
        self.tkvar['blog_path'] = tk.StringVar(value=self.config['blog_path'])
        self.tkvar['secret_id'] = tk.StringVar(value=self.config['secret_id'])
        self.tkvar['secret_key'] = tk.StringVar(value=self.config['secret_key'])
        self.tkvar['github_username'] = tk.StringVar(
            value=self.config['github_username'])
        self.tkvar['github_password'] = tk.StringVar(
            value=self.config['github_password'])
        self.tkvar['gitee_username'] = tk.StringVar(
            value=self.config['gitee_username'])
        self.tkvar['gitee_password'] = tk.StringVar(
            value=self.config['gitee_password'])
        self.tkvar['oss_bucket'] = tk.StringVar(value=self.config['oss_bucket'])
        self.tkvar['oss_region'] = tk.StringVar(value=self.config['oss_region'])
        self.tkvar['cdn_domain'] = tk.StringVar(value=self.config['cdn_domain'])
        self.tkvar['log'] = tk.StringVar(value=self.config['log'])

    def load_config(self):
        try:
            # 读取config.json文件中的配置
            self.config = Config('config.json')
            self.config.load()
        except FileNotFoundError:
            data = {
                'hugo': False,
                'github': False,
                'gitee': False,
                'blog_path': '',
                'tencentcloud_oss': False,
                'tencentcloud_cdn': False,
                'status': '空闲',
                'log': '',
                'files': '',
                'time': '0s',
                'secret_id': '',
                'secret_key': '',
                'github_username': '',
                'github_password': '',
                'gitee_username': '',
                'gitee_password': '',
                'oss_bucket': '',
                'oss_region': '',
                'cdn_domain': '',
                'file_dict':{}
            }
            self.config = Config('config.json', data)
            print("加载配置失败,已创建默认配置")

    def update_files(self, files):
        self.config['files'].set(files)
        
    def update_status(self, status):
        self.config['status'].set(status)

    def update_log(self, log):
        self.config['log'].set(log)

if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()