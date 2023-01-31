---
categories:
- "AI\u5DE5\u5177"
comment: true
date: 2023-01-29 01:47:51+08:00
draft: false
featuredimagepreview: https://blog.hzxwhzxw.asia/featured-image/8.webp
hiddenFromHomePage: false
hiddenFromSearch: false
lightgallery: true
math:
  enable: true
repost:
  enable: true
  url: ''
seo:
  images: []
tags:
- "AI\u5DE5\u5177"
title: "Anaconda\u4F7F\u7528\u6559\u7A0B\uFF08\u4E00\uFF09"
toc:
  enable: true
weight: 0
---
<!--more-->

## Anaconda安装

### Anaconda简介
Anaconda包括Conda、Python以及一大堆安装好的工具包，比如：numpy、pandas等

因此安装Anaconda的好处主要为以下几点：

1）包含conda：conda是一个环境管理器，其功能依靠conda包来实现，该环境管理器与pip类似，那有童鞋会问了：我能通过pip装conda包达到conda环境管理器一样的功能吗？答案是不能，conda包的实现离不开conda环境管理器。想详细知道两者异同可以去知乎遛一遛https://www.zhihu.com/question/279152320

2）安装大量工具包：Anaconda会自动安装一个基本的python，该python的版本Anaconda的版本有关。该python下已经装好了一大堆工具包，这对于科学分析计算是一大便利，你愿意费时耗力使用pip一个个包去装吗？

3）可以创建使用和管理多个不同的Python版本：比如想要新建一个新框架或者使用不同于Anoconda装的基本Python版本，Anoconda就可以实现同时多个python版本的管理

### Anaconda安装情况的选择
Anaconda的安装分两种情况：

情况一：电脑现在没有装python或者现在装的可以卸载掉（装Anaconda时先卸python）；

情况二：电脑目前装了python，但想保留它；

#### 情况一
##### Anaconda的下载
你可以根据你的操作系统是32位还是64位选择对应的版本到官网下载，但是官网下载龟速，建议到清华大学镜像站下载，多快又好省，博主使用的版本是：

Anaconda3-5.2.0-Windows-x86_64.exe

为什么不用最新版的

Anaconda3-5.3.1-Windows-x86_64.exe

不知是版本原因还是什么原因，包括博主在内的一大堆使用这个最新版本在构建虚拟环境或者安装包时出现了这样蛋疼的错误

无法定位程序输入点 OPENSSL_sk_new_reserve 于动态链接库 E：\ProgramData\Anaconda3\Library\bin\libssl-1_1-x64.dll上

最后有博文指出回退3-5.2.0版本毛事木有

下载好Anaconda3后直接双击安装包即可，有几个地方需要注意











Finish后安装完毕

2.1.2 测试安装
cmd输入

conda --version
若出现像这样的conda版本号即安装成功



2.1.3 更改源
使用

conda install 包名
安装需要的Python包非常方便，但是官方服务器在国外，下载龟速，国内清华大学提供了Anaconda的镜像仓库，我们把源改为清华大学镜像源

更改方法一：cmd后依次输入下面命令

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
打开C盘用户目录，我这里是

C:\Users\User
找到.condarc文件，里面长这样就成了

ssl_verify: true
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - defaults
show_channel_urls: true

更改方法二：打开 .condarc文件，直接简单粗暴的把上面的内容复制进去

2.1.4 更新包
更新时间较长，建议找个空余时间更新,不更新也可以，但为避免后续安装其他东西出错最好更一下，这里我就不更了，把命令贴出来

先更新conda

conda update conda
再更新第三方所有包

conda upgrade --all
2.1.5 创建和管理虚拟环境
第一种情况下Anaconda的安装到这里基本就结束了，后面关于虚拟环境部分属于Anaconda的使用了，这里会在第二种情况下再做介绍

2.2 情况二
情况二Anaconda的安装和情况一相同，但为保留自己安装的Python需要在安装Anaconda完成后进行操作

进行操作有2个方法，这里更加推荐方法二

2.2.1 方法一：通过更改python.exe文件名
Anaconda安装时会自带一个Python，没装之前我们先看看电脑里Python的版本（姑且称为原生python），cmd后输入：

python --version 或者 python -V


这里显示原生python版本是3.7.4，我们到环境变量去看是这样的

C:\ProgramFiles\Python37\Scripts\;
C:\ProgramFiles\Python37\;
%SystemRoot%\system32;
%SystemRoot%;
%SystemRoot%\System32\Wbem;
%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\;
C:\Program Files\PuTTY\
按照第一种情况安装Anoconda后再输入

python --version


这时显示的是3.6.5，这里的版本就是Anaconda自带的python版本，我们再打开环境变量

C:\ProgramData\Anaconda3;
C:\ProgramData\Anaconda3\Library\mingww64\bin;
C:\ProgramData\Anaconda3\Library\usr\bin;
C:\ProgramData\Anaconda3\Library\bin;
C:\ProgramData\Anaconda3\Scripts;
C:\ProgramFiles\Python37\Scripts\;
C:\ProgramFiles\Python37\;
%SystemRoot%\system32;
%SystemRoot%;
%SystemRoot%\System32\Wbem;
%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\;
C:\Program Files\PuTTY\
发现原生Python路径还在，同时在原生Python路径之前多了与Anaconda相关的路径，因此Anaconda自带安装的Python并不会覆盖掉原生Python，但为什么输python --version显示的是Anaconda的版本而不是原生的呢？这是因为环境变量优先级的缘故，这里Anaconda在前，原生在后，更改他们的顺序后输入python --version可以得到原生的版本号，有兴趣的童鞋可以自己尝试。

C:\Program Files\Python37;
C:\ProgramFiles\Python37\Scripts\;
C:\ProgramData\Anaconda3;C:\ProgramData\Anaconda3\Library\mingww64\bin;
C:\ProgramData\Anaconda3\Library\usr\bin;
C:\ProgramData\Anaconda3\Library\bin;
C:\ProgramData\Anaconda3\Scripts;
%SystemRoot%\system32;
%SystemRoot%;
%SystemRoot%\System32\Wbem;
%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\;
C:\Program Files\PuTTY\


因此方法一来了，把原生python安装路径下的python.exe改为python_ori.exe



再把Anaconda安装路径下的python.exe改为python_ana.exe



查看版本：



使用时要注意区分，如进行pip安装时

python_ori –m pip install 包名

python_ano –m pip install 包名

2.2.2 方法二：通过切换虚拟环境
输入

conda info -e  或者  conda-env list
查看Anaconda中当前存在的环境



可以看到当前只存在一个叫做base的环境，这个环境即是Anaconda安装的Python版本

Anaconda装的版本是3.6.5的，假如我们想使用2.7版本的，这时可以通过创建虚拟环境来实现，输入

conda create -n python27 python=2.7
不用管是输入2.7.x，还是2.7，conda会为我们自动寻找2.7.x中的最新版本，再次查看Anaconda中存在的环境



发现较之前多了一个python27，我们到Anaconda安装目录查看envs文件夹下的python27



点进去看发现这不就是一个python安装过后的文件吗，说是创建虚拟环境，其实是真实的安装了Python2.7，我们切换至2.7版本的，输入

activate python27
切换成功后前面多一个python27



这时我们保留原生python就有了思路：

1）在Anaconda安装目录下的envi文件内新建一个名为python_ori的文件（没有envs文件夹就自己新建）

2）将原生python整个安装目录复制python_ori



3）全部复制后粘贴到python_ori



4）cmd后激活切换至原生的python



查询版本号



没问题，3.7.4是原生版本，那是那个味哈哈。

## Anacoda环境创建

