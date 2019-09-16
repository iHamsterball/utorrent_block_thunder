
# μTorrent 迅雷自动屏蔽脚本

> 以其他语言阅读此文章：[English](/docs/en_us.md), [简体中文](/docs/zh_cn.md)

## 简介

定时检查 μTorrent 已连接的用户列表，将迅雷相关客户端所属 IP 加入 IPFilter 文件。

### 屏蔽客户端列表

- -XL0012-***
- Xunlei/***
- 7.x.x.x
- Xfplay

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

> **前置要求：安装 [μTorrent WebUI](https://forum.utorrent.com/topic/49588-μtorrent-webui/)**

### 直接执行

``` sh
python main.py
```

### 作为 Windows Service 执行

WIP

## 参考

[uTorrent 自动屏蔽迅雷脚本(uTorrent block xunlei/thunder)](https://www.v2ex.com/t/509327)
