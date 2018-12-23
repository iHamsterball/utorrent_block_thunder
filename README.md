# uTorrent 自动屏蔽迅雷脚本
## 功能

每隔 60 秒，自动检查 uTorrent 已连接的用户列表，找出迅雷客户端，强制断开，不给吸血雷上传任何数据，并将用户 IP 加入黑名单阻止其再次连接，把带宽留给正规 BT 客户端。

## 屏蔽列表

-XL0012-***

Xunlei/***

7.x.x.x

Xfplay


## 实现方法

1.  根据 uTorrent 的 WebUI API 发送 http request 获取所有已连接用户(peers)信息
2.  按照 client name 筛选出使用迅雷的 peer IP，写入 ipfilter.dat 文件
3.  发送 http request 让 uTorrent 重新加载 ipfilter.dat
4.  uTorrent 禁止 ipfilter.dat 中的 IP 连接

## 脚本

基于python 3.7

python库 requests

# 自行修改脚本中 root_url, auth, ipfilter_path 相关内容

ut  过滤文件地址 请修改 109行 fileAddress （请先在对应目录新建一个空的ipfilter.dat）


url 访问http连接 请修改 110行 Root_url


ut开启webui访问  设置用户：1  密码：1  （这个没搞定，写死了，就是headers）



然后在当前项目界面打开cmd，运行python main.py

# 检查间隔时间可在脚本中自定义，IP黑名单(ipfilter.dat) 建议每天清空一次。


完全照搬SHF大佬的思路，感谢大佬的辛苦付出。

https://www.v2ex.com/t/509327

https://github.com/ShenHongFei/utorrent-block-xunlei





