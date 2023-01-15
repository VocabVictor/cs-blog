# -*- coding: utf-8 -*-
# !/usr/bin/python3
# @Time    : 2023/1/8 15:00
# @Author  : VocabVictor
# @Email   : vocabvictor@gmail.com
# @File    : update.py
# @Software: PyCharm,VsCode
# @Description: 用于安全读取和保存markdown文件
# @Support Python Version: 3.5+
# 以下是一个Markdown类，用于安全读取和保存markdown文件，他的功能是：
'''
    1. 读取markdown文件，如果markdown文件不存在，则创建一个新的markdown文件；如果markdown文件存在，则读取markdown文件
    2. 保存markdown文件，如果markdown文件不存在，则创建一个新的markdown文件；如果markdown文件存在，则覆盖markdown文件
    3. 读取markdown文件中的内容时，把markdown文件中的Front Matter部分读取出来，并把markdown文件中的正文部分读取出来
    4. 读取出来的Front Matter部分是一个字典，可以通过字典的方式访问Front Matter部分的内容
'''
from os.path import exists
from yaml import safe_load as yaml_load, safe_dump as yaml_dump
from os import listdir
from random import choice

class Markdown:
    def __init__(self, blog_path = None,filename = None):
        self.filename = filename
        self.blog_path = blog_path
        self.front_matter = {}
        self.content = ''
        self.featured_image_dir = 'static/featured-image'
        self.featured_images = []
        self.image_types = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp')
        self.featured_image_prefix = '/featured-image/'
        self.init_featured_image()
        self.default_front_matter = {
            'math': {
                'enable': True
            },
            'draft': False,
            'lightgallery': True,
            'comment': True
        }

    # 设置markdown文件路径函数
    def set_path(self, filename):
        self.filename = filename
        self.read()

    # 初始化featured_images数组函数
    def init_featured_image(self):
        # 初始化featured_images数组，把featured_image_dir目录下的所有文件名都放到featured_images数组中
        featured_image_dir = self.blog_path + "/" + self.featured_image_dir
        # 检查featured_image_dir目录是否存在，如果存在，则把featured_image_dir目录下的所有图片文件名都放到featured_images数组中
        if exists(featured_image_dir):
            self.featured_images = [ 
                self.featured_image_prefix + i 
                for i in listdir(self.featured_image_dir) 
                    if i.endswith(self.image_types)
            ]        

    # 读取markdown文件函数
    def read(self,filename=None):
        # filename参数是可选参数，如果不传入filename参数，则使用self.filename
        filename = filename or self.filename
        # 如果markdown文件不存在，则创建一个新的markdown文件
        if exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('---'):
                    _ , front_matter, content = content.split('---', 3)
                    if front_matter:
                        self.front_matter = yaml_load(front_matter)
                self.content = content.strip()
        else:
            # 创建一个新的markdown文件
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('')

    # 保存markdown文件函数，并把外部传入的字典数据写入到markdown文件中的Front Matter部分
    # 对于Front Matter部分的默认设置规则如下
    '''
        1. 如果外部传入的字典数据中的key在Front Matter部分中不存在，则把外部传入的字典数据中的key和value写入到Front Matter部分中
        2. 如果外部传入的字典数据中的key在Front Matter部分中存在，则把外部传入的字典数据中的key和value覆盖Front Matter部分中的key和value
        3. 删除掉Front Matter部分中的空字符串
        4. 删除掉Front Matter部分中的list中的空字符串
        5. 删除掉Front Matter部分中的resources
        6. 强制Front Matter部分中的math.enable为true,draft为false
        7. 强制Front Matter部分中的lightgallery为true
        8. 强制Front Matter部分中的comments为true
    '''  
    def write(self,data = {},filename=None):
        # filename参数是可选参数，如果不传入filename参数，则使用self.filename
        filename = filename or self.filename
        # 遍历外部传入的字典数据，把外部传入的字典数据写入到Front Matter部分中
        for key in data:
            if data[key] != '':
                self.front_matter[key] = data[key]
    
        # 删除掉Front Matter部分中list的空字符串,寻找空字符串对应的key
        keys = ["resources"]
        for key in self.front_matter:
            # 去掉空字符串
            if self.front_matter[key] == '':
                keys.append(key)  
            elif isinstance(self.front_matter[key],list):
                # 去掉list中的空字符串
                self.front_matter[key] = [i for i in self.front_matter[key] if i]
        
        # 删除掉Front Matter部分中空字符串对应的键值对
        self.front_matter = {key:self.front_matter[key] for key in self.front_matter if key not in keys}

        # 把默认的Front Matter部分的key和value写入到Front Matter部分中
        for key in self.default_front_matter:
            self.front_matter[key] = self.default_front_matter[key]

        # 如果Front Matter部分中的featured_image为空字符串，则把featured_image设置为featured_images数组中的随机一个文件名
        if self.front_matter.get('featuredimagepreview',"") == "":
            self.front_matter['featuredimagepreview'] = choice(self.featured_images)

        # 把修改后的Front Matter部分和content部分写入到markdown文件中
        with open(filename, 'w', encoding='utf-8') as f:
            if self.front_matter:
                f.write('---\n')
                f.write(yaml_dump(self.front_matter, default_flow_style=False))
                f.write('---\n')
            f.write(self.content)
    
if __name__ == "__main__":
    # 实例化Markdown类
    md = Markdown("F:\\cs-blog",r"F:\cs-blog\content\posts\毕业设计.md")
    # # 读取markdown文件
    md.read()
    md.write(data = {"title":"毕业设计","categories":["毕业设计"],"tags":["毕业设计"]})
    