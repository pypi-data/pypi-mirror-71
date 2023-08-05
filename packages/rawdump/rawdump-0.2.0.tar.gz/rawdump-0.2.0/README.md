
```
  _____                _____                        
 |  __ \              |  __ \                       
 | |__) |__ ___      _| |  | |_   _ _ __ ___  _ __  
 |  _  // _` \ \ /\ / / |  | | | | | '_ ` _ \| '_ \ 
 | | \ \ (_| |\ V  V /| |__| | |_| | | | | | | |_) |
 |_|  \_\__,_| \_/\_/ |_____/ \__,_|_| |_| |_| .__/ 
                                             | |    
                                             |_|  
```

![Unittest](https://github.com/drunkdream/rawdump/workflows/Unittest/badge.svg)
[![PyPi version](https://img.shields.io/pypi/v/rawdump.svg)](https://pypi.python.org/pypi/rawdump/) 

## 已实现功能

* 支持Windows、Linux、Macos端抓包
* 支持根据网卡、协议、ip、端口、包体中的关键字等进行过滤（过滤以流为单位）
* 支持生成pcap文件

## 待实现功能

* 支持过滤包含RST包的流
* 支持字体染色

## 使用方法

```bash
$ pip install rawdump
$ rawdump -i lo -H ip -P port --keyword test -w 1.pcap
```

参数说明：

* `-i/--interface`: 指定要抓包的网卡，Windows系统使用网卡序号，其它系统使用网卡名；不指定会抓所有网卡包

* `-p/--protocol`: 要过滤的协议，如：tcp、udp、icmp，默认抓所有ip包

* `-H/--host`: 要过滤的ip地址

* `-P/--port`: 要过滤的端口（只支持TCP和UDP）

* `--keyword`: 要过滤的关键字

* `-w/--file`: 要保存的文件名，默认值为：rawdump.pcap

## 使用限制

Windows下需要`Administrator`权限，其它系统需要`root`权限。
