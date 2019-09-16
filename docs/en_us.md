# μTorrent Thunder Auto-block Script

> Read this article in other languages: [简体中文](docs/zh_cn.md)

## Briefing

Check μTorrent connected peers periodically, and add IPs whose client matches Thunder etc. to IPFilter.

### Blocked client list

- -XL0012-***
- Xunlei/***
- 7.x.x.x
- Xfplay

### Mechanisim

> Replica of manual operation basically

1. Fetch complete peers list by sending HTTP request according to WebUI API of μTorrent
2. Filter IPs that using Thunder, and write to ipfilter.dat file
3. Reload IPFilter by sending HTTP request

## Configuration

- Modify `protocal`, `domain`, `port`, `path`, `user`, `password` fields according your own configuration of WebUI.
- Currently `ipfilter_path` could automatically fetch default installation path on Windows. If μTorrent is not installed at default path, or you are using Linux / MacOS, please modify the field to absolute path.
- Modify `interval` field on your need, default 30 seconds, interger in seconds.

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

## Usage

> **Presequence：Install WebUI**
> [μTorrent WebUI - Web API - μTorrent Community Forums](https://forum.utorrent.com/topic/49588-μtorrent-webui/)

### Run directly

``` sh
python main.py
```

### Run as Windows Service

WIP

## References

[uTorrent 自动屏蔽迅雷脚本(uTorrent block xunlei/thunder](https://www.v2ex.com/t/509327)