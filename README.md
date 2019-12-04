# TeleNote

[![GitHub issues](https://img.shields.io/github/issues/ds19991999/TeleNote.svg)](https://github.com/ds19991999/TeleNote/issues)
[![DUB](https://img.shields.io/dub/l/vibe-d.svg)](https://github.com/ds19991999/TeleNote/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/release/ds19991999/TeleNote.svg)](https://github.com/ds19991999/TeleNote/releases)
[![Badge](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu/#/zh_CN)
[![GitHub stars](https://img.shields.io/github/stars/ds19991999/TeleNote.svg?style=popout&label=Stars)](https://github.com/ds19991999/TeleNote/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ds19991999/TeleNote.svg?style=popout&label=Fork)](https://github.com/ds19991999/TeleNote/fork)

[`telenote`](https://github.com/ds19991999/TeleNote) 使用 [`telegraph`](https://telegra.ph) 构建。[`telegraph`](https://telegra.ph) 官网无法编辑已发布的文章，并且没有提供账户管理，文章管理，于是该脚本应用诞生，通过使用唯一的 `access_token`创建文章，使用 `auth_url` 获取历史文章的编辑权限。目前，该应用还未正式开发，未来将构建客户端笔记应用，先留个坑吧 。。。

## 环境


```shell
git clone https://github.com/ds19991999/TeleNote.git
python3 -m pip install requests[socks]==2.22.0
```

## 配置

新建 `config.yaml` 文件，填写相关参数。

## 运行

`cmd` 直接运行即可，代理需要配置正确，否则会抛出 `requests.exceptions.ConnectionError` 异常。

![image-20191204195252105](assets/image-20191204195252105.png)

![image-20191204195327778](assets/image-20191204195327778.png)

![image-20191204195350787](assets/image-20191204195350787.png)



## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>