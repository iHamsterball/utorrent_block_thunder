
# μTorrent 迅雷自动屏蔽脚本

> 以其他语言阅读此文章：[English](/docs/en_us.md), [简体中文](/docs/zh_cn.md)

---

![GitHub](https://img.shields.io/github/license/iHamsterball/utorrent_block_thunder)
![GitHub top language](https://img.shields.io/github/languages/top/iHamsterball/utorrent_block_thunder)
![Requires.io](https://img.shields.io/requires/github/iHamsterball/utorrent_block_thunder)

定时检查 μTorrent 已连接的用户列表，将迅雷相关客户端所属 IP 加入 IPFilter 文件。

## 简介

### 屏蔽客户端列表

#### 无条件屏蔽

- -XL0012-***
- Xunlei/***
- 7.x.x.x
- QQDownload
- Xfplay
- dandanplay

#### 有条件屏蔽

> 如果用户下载量超过种子大小则屏蔽

- FDM
- Mozilla
- go.torrent

#### 其他

> 如果用户下载量超过种子大小 2 倍则屏蔽

#### 例外

> 如果一个用户上传了任意数量的数据，无论其客户端是什么都不会被屏蔽

### 工作机制

> 基本上就是复刻手动操作流程

1. 根据 μTorrent 的 WebUI API 发送 HTTP 请求获取所有已连接用户信息
2. 根据 Peer 的 Client 字段筛选出使用迅雷的 IP，写入 ipfilter.dat 文件
3. 发送 HTTP 请求，让 μTorrent 重新加载 IPFilter

## 配置

- `protocal`, `domain`, `port`, `path`, `user`, `password` 字段根据自己的 WebUI 配置修改
- `ipfilter_path` 可以从 Windows 设备上获取默认安装地址，如果没有安装在默认安装路径，或者使用 Linux / MacOS 设备，请自行修改为绝对路径
- `interval` 字段为以秒为单位的间隔时间，默认 30 秒，根据自己需要修改

``` python
protocal = 'http'
domain = 'localhost'
port = 43202
path = '/gui'
user = 'root'
password = 'toor'
ipfilter_path = os.path.join(os.getenv('appdata'), 'uTorrent', 'ipfilter.dat')
interval = 30
```

## 用法

> **前置要求：安装并启用 [μTorrent 网页界面](https://forum.utorrent.com/topic/49588-μtorrent-webui/)**

### 直接执行

``` sh
python main.py
```

### 作为 Windows Service 执行

WIP

## 注意

强烈建议事先备份你本来的 `ipfilter.dat` 文件，在脚本执行过程中存在清空 `ipfilter.dat` 文件可能。

## 许可

``` plaintext
Code & Documentation 2019 © Cother
Code released under the Apache 3.0 license
Docs released under Creative Commons (CC BY-SA 4.0)
```

## 参考

[uTorrent 自动屏蔽迅雷脚本(uTorrent block xunlei/thunder)](https://www.v2ex.com/t/509327)  
[Torrent/Labels List Definition](http://help.utorrent.com/customer/portal/articles/1573947)
