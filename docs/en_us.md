# μTorrent Thunder Auto-block Script

> Read this article in other languages: [English](/docs/en_us.md), [简体中文](/docs/zh_cn.md)

---

![GitHub](https://img.shields.io/github/license/iHamsterball/utorrent_block_thunder)
![GitHub top language](https://img.shields.io/github/languages/top/iHamsterball/utorrent_block_thunder)
![Requires.io](https://img.shields.io/requires/github/iHamsterball/utorrent_block_thunder)

Check μTorrent connected peers periodically, and add IPs whose client matches Thunder etc. to IPFilter.

## Briefing

### Blocked client list

#### Unconditionally block

- -XL0012-***
- Xunlei/***
- 7.x.x.x
- QQDownload
- Xfplay
- dandanplay

#### Conditionally block

> Block if peer downloaded more than torrent size

- FDM
- Mozilla
- go.torrent

#### Others

> Block if peer downloaded more than twice times torrent size

#### Exception

> It won't be blocked no matter what the client is if a peer has uploaded any amount of data

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

> **Presequence: Install and enable [μTorrent WebUI](https://forum.utorrent.com/topic/49588-μtorrent-webui/)**

### Run directly

``` sh
python main.py
```

### Run as Windows Service

WIP

## Caution

It is highly recommended to backup your original `ipfilter.dat` file before using this script. Your `ipfilter.dat` file might be emptied during the execution.

## License

``` plaintext
Code & Documentation 2019 © Cother
Code released under the Apache 3.0 license
Docs released under Creative Commons (CC BY-SA 4.0)
```

## References

[uTorrent 自动屏蔽迅雷脚本(uTorrent block xunlei/thunder)](https://www.v2ex.com/t/509327)  
[Torrent/Labels List Definition](http://help.utorrent.com/customer/portal/articles/1573947)
