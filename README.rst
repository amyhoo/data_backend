介绍
============
数据后台实现，提供前台的数据存取查看工作。
使用REST api方式，使用route，webob包封装
数据库为sqlachemy
客户端可以使用requests接口获取数据
安装使用
---------
* 下载解压到本地目录下
* 本程序是一个框架

组成
----------
* controller:逻辑层，将http参数，数据信息转化为底层控制。
* db：数据库存取
* emailsms:自动发送邮件短信提醒
* urlmap: url的路由

接口描述 (alipay/alipay.py)
---------
分布式数据后台框架


